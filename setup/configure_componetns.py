#!/usr/bin/env python3
#

# import modules used here -- sys is a very standard one
import sys,argparse,os,subprocess

from lxml import html
import requests
import urllib.request
import tempfile
import re
import pexpect
from libtbngsetup import *

def configure_tor(torrc):
  token="tbng enabled settings"
  settings="""Log notice syslog
VirtualAddrNetworkIPv4 10.192.0.0/10
AutomapHostsOnResolve 1
TransPort 0.0.0.0:9040
DNSPort 0.0.0.0:9053
CircuitBuildTimeout 30
KeepAlivePeriod 60
NewCircuitPeriod 15
NumEntryGuards 8
ConstrainedSockets 1
ConstrainedSockSize 8192
AvoidDiskWrites 1
SocksPort 0.0.0.0:9050"""
  utility.removeFileData(torrc,prefix,token)
  utility.appendFileData(torrc,prefix,token,settings)
  logging.debug(utility.run_multi_shell_command("systemctl restart tor").decode("utf-8"))

def configure_privoxy(privoxyconf):
  utility.replace_string_in_file(privoxyconf,"listen-address  localhost:8118","#listen-address  localhost:8118")
  utility.replace_string_in_file(privoxyconf,"listen-address  127.0.0.1:8118","#listen-address  127.0.0.1:8118")
  utility.replace_string_in_file(privoxyconf,"listen-address  [::1]:8118","#listen-address  [::1]:8118")
  utility.replace_string_in_file(privoxyconf,"enable-remote-toggle  0","#enable-remote-toggle  0")
  utility.replace_string_in_file(privoxyconf,"enable-edit-actions 0","#enable-edit-actions 0")
  utility.replace_string_in_file(privoxyconf,"accept-intercepted-requests 0","#accept-intercepted-requests 0")
  
  token="tbng enabled settings"
  settings="""listen-address 0.0.0.0:8118
enable-remote-toggle 1
enable-edit-actions 1
accept-intercepted-requests 1
forward-socks4a / 127.0.0.1:9050 .
forward          .i2p            127.0.0.1:4444
forward-socks4a  .onion          127.0.0.1:9050 ."""
  utility.removeFileData(privoxyconf,prefix,token)
  utility.appendFileData(privoxyconf,prefix,token,settings)
  logging.debug(utility.run_multi_shell_command("systemctl restart privoxy").decode("utf-8"))

def download_i2p():
  page = requests.get('https://geti2p.net/en/download')
  tree = html.fromstring(page.content)

  version_url = tree.xpath('//div[@id="unix"]/div[@class="details"]/div[@class="file"]/a[@class="default"]/@href')[0]

  version = re.search('i2pinstall_(.+?).jar', version_url).group(1)

  filename = "{0}_i2pinstall_{1}.jar".format(tempfile.mktemp(),version)
  url="http://download.i2p2.de/releases/{0}/i2pinstall_{0}.jar".format(version)

  logging.info("""Downloading from {0}
  to {1}
  """.format(url,filename))
  urllib.request.urlretrieve(url,filename)
  
  return filename  

def install_i2p(filename):

  #Install code here
  #systemd stuff also
  logging.info("Trying to kill running i2p if any")
  killer="""if [ -f /tmp/router.pid ]; then
  kill `cat /tmp/router.pid` || true
  sleep 10
fi  
rm -rf {0}/i2p || true
rm -rf ~{0}/.i2p""".format(project_dir)

  logging.debug(utility.run_multi_shell_command(killer).decode("utf-8"))
  logging.debug("Installing from {0}".format(filename))
  command_line = "java -jar {0} -console".format(filename)
  location = "{0}/i2p".format(project_dir)
  os.mkdir(location)
  child = pexpect.spawn(command_line)
  child.expect("Input selection:",timeout=60)
  child.sendline("0")
  child.expect("Press 1 to continue, 2 to quit, 3 to redisplay",timeout=60)
  child.sendline("1")
  child.expect("Press 1 to continue, 2 to quit, 3 to redisplay",timeout=60)
  child.sendline("1")
  child.expect("Select the installation path:.*",timeout=60)
  child.sendline(location)
  child.expect("Enter O for OK, C to Cancel:",timeout=60)
  child.sendline("O")
  child.expect("Press 1 to continue, 2 to quit, 3 to redisplay",timeout=60)
  child.sendline("1")
  child.expect("Press 1 to continue, 2 to quit, 3 to redisplay",timeout=60)
  child.sendline("1")
  child.expect(".*Console installation done.*",timeout=60)
  child.sendline("")

  logging.debug(utility.run_shell_command("chown -R {0}:$(id {0} -gn) {1}".format(args.user,location)).decode("utf-8"))

  try:
    os.remove(filename)
  except OSError:
    pass


# Gather our code in a main() function
def main(args, loglevel):

  parameters={}
  parameters['project']=project_dir
  parameters['user']=args.user

  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
  logging.debug("Arguments passed: user {0}, tor config file {1}, privoxy config file {2}".format(args.user,args.torrc,args.privoxyconf))

  logging.info("Checking user {0}".format(args.user))
  if  args.user == "root":
    raise Exception("DO NOT use root account for TBNG.")

  logging.debug(utility.run_shell_command("getent passwd {0}".format(args.user)).decode("utf-8"))

  logging.info("Adding user to sudoers for TBNG engine")
  token="run engine without password"
  utility.removeFileData("/etc/sudoers",prefix,token)
  utility.appendFileData("/etc/sudoers",prefix,token,"{0} ALL=NOPASSWD: {1}/engine/tbng.py".format(args.user,project_dir))

  logging.info("Configuring tor")
  configure_tor(args.torrc)

  logging.info("Configuring privoxy")
  configure_privoxy(args.privoxyconf)
  
  logging.info("Downloading i2p")
  i2p_package=download_i2p()

  logging.info("Installing i2p")
  install_i2p(i2p_package)
  toSystemd("i2p-tbng.service",parameters)
  logging.info("Starting i2p and doing initial configuration")
  command="""systemctl start i2p-tbng
sleep 20
systemctl stop i2p-tbng
su -c "sed -i 's/clientApp.0.args=7657\s*::1,127.0.0.1\s*.\/webapps\//clientApp.0.args=7657 0.0.0.0 .\/webapps\//' ~{0}/.i2p/clients.config" {0}
su -c "sed -i 's/clientApp.4.startOnLoad=true/clientApp.4.startOnLoad=false/'  ~{0}/.i2p/clients.config" {0}"""
  logging.debug(utility.run_multi_shell_command(command.format(args.user)).decode("utf-8"))
  
   
  logging.info("Doing npm install for webui")
  command='su - {0} -c "cd {1} && npm install"'.format(args.user,project_dir)
  logging.debug(utility.run_shell_command(command).decode("utf-8"))

  logging.info("Configuring autostart for tbng-helper")
  toSystemd("tbng.service",parameters,True)

  logging.info("Configuring autostart for webui-tbng")
  toSystemd("webui-tbng.service",parameters,True)
  
  logging.info("Checking TBNG configuration")
  try:
    logging.debug(utility.run_shell_command("{0}/engine/tbng.py chkconfig".format(project_dir)).decode("utf-8"))
  except subprocess.CalledProcessError as e:
    message="""There was en error checking your configuraiotn:
 - your file config/tbng.json is not found
 - your system is not configured
Fix config file and run engine/tbng.py chkconfig to check config manually.
After this you can proceed with reboot and start using your system."""
    logging.info(message)
    logging.info("Original error message:\n{0}".format(e.output))
  else:
    logging.debug(utility.run_shell_command("sync").decode("utf-8"))
    logging.info("Configuration done. Powercycle your system and connect to http://your.ip.address:3000 via browser")
      


# Standard boilerplate to call the main() function to begin
# the program.

if sys.version_info[0] < 3:
    raise Exception("Python 3.x is required.")

if not os.geteuid()==0:
 raise Exception("sudo or root is required.")

if __name__ == '__main__':
  parser = argparse.ArgumentParser( 
                                    description = "Components configurator for TBNG project."
                                  )

  parser.add_argument('-u',
                      '--user',
                       type=str, help='Non-root username to use',required=True)
  parser.add_argument('-t',
                      '--torrc',
                       type=str, default="/etc/tor/torrc", help="Path to TOR torrc file")
 
  parser.add_argument('-p',
                      '--privoxyconf',
                      type=str, default="/etc/privoxy/config", help="Path to Privoxy config file")
 
  parser.add_argument(
                      "-v",
                      "--verbose",
                      help="increase output verbosity",
                      action="store_true")
  args = parser.parse_args()
  # Setup logging
  if args.verbose:
    loglevel = logging.DEBUG
  else:
    loglevel = logging.INFO

if sys.version_info[0] < 3:
  raise Exception("Python 3.x is required.")

if not os.geteuid()==0:
  raise Exception("sudo or root is required.")
  
main(args, loglevel)

#!/usr/bin/env python3
#

# import modules used here -- sys is a very standard one
import sys,argparse,logging,os,json,subprocess
from pathlib import Path

from lxml import html
import requests
import urllib.request
import tempfile
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = Path(current_dir).parent

sys.path.insert(0,'{0}/engine'.format(project_dir))
from libraries import utility

def download_i2p():
  page = requests.get('https://geti2p.net/en/download')
  tree = html.fromstring(page.content)

  version_url = tree.xpath('//div[@id="unix"]/div[@class="details"]/div[@class="file"]/a[@class="default"]/@href')[0]

  version = re.search('i2pinstall_(.+?).\jar', version_url).group(1)

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
  logging.debug("Installing from {0}".format(filename))
  try:
    os.remove(filename)
  except OSError:
    pass


# Gather our code in a main() function
def main(args, loglevel):
  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
  logging.debug("Arguments passed: user {0}, tor config file {1}, privoxy config file {2}".format(args.user,args.torrc,args.privoxyconf))

  logging.info("Checking user {0}".format(args.user))
  logging.debug(utility.run_shell_command("getent passwd {0}".format(args.user)))

  logging.info("Adding user to sudoers for TBNG engine")
  utility.appendFileData("/etc/sudoers","#Added by TBNG setup - do not edit ","run engine without password","{0} ALL=NOPASSWD: {1}/engine/tbng.py".format(args.user,project_dir))

  logging.info("Configuring tor")

  logging.info("Configuring privoxy")
  
  logging.info("Downloading i2p")
  i2p_package=download_i2p()

  logging.info("Installing i2p")
  install_i2p(i2p_package)
   
  logging.info("Doing npm install for webui")
  command='su - {0} -c "cd {1} && npm install"'.format(args.user,project_dir)
  logging.debug(utility.run_shell_command(command))

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

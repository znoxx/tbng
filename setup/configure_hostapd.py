#!/usr/bin/env python3
#

# import modules used here -- sys is a very standard one
import sys,argparse,logging,os,json,subprocess
from pathlib import Path

import urllib.request
import tempfile
import re
import gzip
from string import Template

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = Path(current_dir).parent

sys.path.insert(0,'{0}/engine'.format(project_dir))
from libraries import utility

prefix="#Added by TBNG setup - do not edit "

def toSystemd(name,parameters,autostart=False):
  systemd_folder="/lib/systemd/system"
  filein = open( "templates/{0}".format(name) )
  src = Template( filein.read() )
  src.substitute(parameters)
  with open("{0}/{1}".format(systemd_folder,name), "w") as text_file:
    text_file.write(src.substitute(parameters))
  logging.info("File {0}/{1} created".format(systemd_folder,name))
  logging.debug(utility.run_shell_command("systemctl daemon-reload").decode("utf-8"))
  if autostart:
    logging.debug(utility.run_shell_command("systemctl enable {0}".format(name)).decode("utf-8"))


# Gather our code in a main() function
def main(args, loglevel):

  

  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
  logging.debug("Arguments passed: {0}".format(args))

  parameters={}
  parameters['project']=project_dir
  parameters['interface']=args.interface
  parameters['apname']=args.apname
  parameters['appassword']=args.appassword
  parameters['driver']=args.driver

  logging.info("Checking arguments")
  if len(args.appassword) < 8:
    raise Exception("Access point password must be 8 symbols or more")
  

  if args.dnsmasq not in ["none","apt","yum"]:
    raise Exception("apt,yum,none options for dnsmasq are allowed")

  
  if args.dnsmasq not in ["none"]:
    if (args.dhcpbegin == "none") or (args.dhcpend == "none") or (args.dhcpmask == "none"):
      raise Exception("DHCP start, end and mask must be provided") 

  logging.info("Checking {0} is configured manually".format(args.interface))

  command="nmcli dev show {0}|grep unmanaged||true".format(args.interface)
  if "unmanaged" not in utility.run_shell_command(command).decode("utf-8"):
     raise Exception("""Interface {0} appears to be managed or not configured. 
Configure it via /etc/network/interfaces to have static ip and restart Network Manager or reboot your device.""".format(args.interface))

  filename = "{0}_hostapd.gz".format(tempfile.mktemp())
  url="http://static-bins.herokuapp.com/files/{0}/hostapd/hostapd.gz".format(args.arch)

  logging.info("""Downloading from {0}
  to {1}
  """.format(url,filename))
  urllib.request.urlretrieve(url,filename)

  logging.info("Extracting archive")
  with gzip.open(filename, "rb") as compressed_file:
    with open("{0}/bin/hostapd-tbng".format(project_dir),"wb") as uncompressed_file:
      uncompressed_file.write(compressed_file.read())
  logging.debug(utility.run_shell_command("chmod a+x {0}/bin/hostapd-tbng".format(project_dir)).decode("utf-8"))

  logging.info("Generating hostapd config file")
  filein = open("{0}/setup/templates/hostapd-tbng.conf".format(project_dir))
  src = Template( filein.read() )
  src.substitute(parameters)
  with open("{0}/config/hostapd-tbng.conf".format(project_dir), "w") as text_file:
    text_file.write(src.substitute(parameters)) 

  logging.info("Generating systemd file")
  systemd_folder="/lib/systemd/system"
  filein = open( "{0}/setup/templates/hostapd-tbng.service".format(project_dir))
  src = Template( filein.read() )
  src.substitute(parameters)
  with open("{0}/hostapd-tbng.service".format(systemd_folder), "w") as text_file:
    text_file.write(src.substitute(parameters))
  logging.info("File {0}/hostapd-tbng.service created".format(systemd_folder))
  logging.debug(utility.run_shell_command("systemctl daemon-reload").decode("utf-8"))
  logging.debug(utility.run_shell_command("systemctl enable hostapd-tbng").decode("utf-8")) 

  logging.info("Installing dnsmasq package")
  if args.dnsmasq in ["apt","yum"]:
    if (args.dnsmasq == "apt"):
      logging.debug(utility.silently_install_by_apt("dnsmasq").decode("utf-8"))
    elif (args.dnsmasq == "yum"):
     logging.debug(utility.silently_install_by_yum("dnsmasq").decode("utf-8"))
  
    logging.info("Configuring dnsmasq")
    settings = """interface={0}
dhcp-range={1},{2},{3},12h""".format(args.interface,args.dhcpbegin,args.dhcpend,args.dhcpmask)
    utility.removeFileData("/etc/dnsmasq.conf",prefix,"AP settings")
    utility.appendFileData("/etc/dnsmasq.conf",prefix,"AP settings",settings)
    logging.debug(utility.run_multi_shell_command("systemctl restart dnsmasq").decode("utf-8"))

  logging.debug(utility.run_shell_command("sync").decode("utf-8"))
  logging.info("Device configured. Powercycle your system and try to connect to new access point")
      


# Standard boilerplate to call the main() function to begin
# the program.

if sys.version_info[0] < 3:
  raise Exception("Python 3.x is required.")

if not os.geteuid()==0:
  raise Exception("sudo or root is required.")

if __name__ == '__main__':
  parser = argparse.ArgumentParser( 
                                    description = "Script to configure static version of hostapd. Use with caution."
                                  )

  parser.add_argument('-a',
                      '--arch',
                       type=str, help='Architecture (armh,aarch65,x86,x86_64,...)',required=True)

  parser.add_argument('-i',
                      '--interface',
                       type=str, help="Interface name (wlan0,wlan1,...)",required=True)

  parser.add_argument('-n',
                      '--apname',
                       type=str, help="Access point name",required=True)

  parser.add_argument('-p',
                      '--appassword',
                       type=str, help="Access point password (must be 8+ symbols)",required=True)
  
  parser.add_argument('-s',
                      '--dnsmasq',
                       type=str, default="none",help="Configure dnsmasq. Possible values are apt (install from apt),yum (install from yum) or none (default - no config will be made)")
  
  parser.add_argument('-b',
                      '--dhcpbegin',
                       type=str, default="none", help="DHCP start address, used to configure dnsmasq service. Not validated!")

  parser.add_argument('-e',
                      '--dhcpend',
                       type=str, default="none", help="DHCP end address, used to configure dnsmasq service. Not validated!")
  
  parser.add_argument('-m',
                      '--dhcpmask',
                       type=str, default="none", help="DHCP mask, used to configure dnsmasq service. Not validated!")                       
 
  parser.add_argument('-d',
                      '--driver',
                      type=str, default="nl80211", help="Driver for hostapd. Default is nl80211, also possible rtl871xdrv for Realtek cards")
 
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

#if not os.geteuid()==0:
#  raise Exception("sudo or root is required.")
  
main(args, loglevel)

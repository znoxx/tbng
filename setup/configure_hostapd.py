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
  logging.debug(utility.run_shell_command("systemctl daemon-reload"))
  if autostart:
    logging.debug(utility.run_shell_command("systemctl enable {0}".format(name)))


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

  if len(args.appassword) < 8:
    raise Exception("Access point password must be 8 symbols or more")
  

  if args.dnsmasq not in ["none","apt","yum"]:
    raise Exception("apt,yum,none options for dnsmasq are allowed")

  
  if args.dnsmasq not in ["none"]:
    if (args.dhcpbegin == "none") or (args.dhcpend == "none"):
      raise Exception("DHCP start and addresses must be provided") 


  #Check the interface in unmanaged and up via nmcli

  filename = "{0}_hostapd.gz".format(tempfile.mktemp())
  url="http://static-bins.herokuapp.com/{0}/hostapd/hostapd.gz".format(args.arch)

  logging.info("""Downloading from {0}
  to {1}
  """.format(url,filename))
  urllib.request.urlretrieve(url,filename)


  with gzip.open(filename, "rb") as compressed_file:
    with open("{0}/bin/hostapd-tbng".format(project_dir),"wb") as uncompressed_file:
      uncompressed_file.write(compressed_file.read())


  filein = open("templates/hostapd-tbng.conf")
  src = Template( filein.read() )
  src.substitute(parameters)
  with open("{0}/config/hostapd-tbng.conf".format(project_dir), "w") as text_file:
    text_file.write(src.substitute(parameters)) 

  #Generate hostapd service and push it to folder

  #Silently install dnsmasq from yum or apt

  #Configure dnsmasq with settings

  #Report, advice to reboot 
      


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

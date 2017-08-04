"""
Common functions for setup.
Usage:
from libtbngsetup import *

Do not relocate to subfolder.Requires Python 3.x
"""

import sys,logging,os
from pathlib import Path
from string import Template
import netifaces as ni
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = Path(current_dir).parent
sys.path.insert(0,'{0}/engine'.format(project_dir))
from libraries import utility

prefix="#Added by TBNG setup - do not edit "

def check_interface(interface_name):
  command="nmcli dev show {0}|grep unmanaged||true".format(interface_name)
  if "unmanaged" not in utility.run_shell_command(command).decode("utf-8"):
     raise Exception("""Interface {0} appears to be managed or not configured.
Configure it via /etc/network/interfaces to have static ip and restart Network Manager or reboot your device.""".format(interface_name))
  return ni.ifaddresses(interface_name)[2][0]['addr']

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

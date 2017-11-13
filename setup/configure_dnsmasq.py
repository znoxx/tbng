#!/usr/bin/env python3
#

# import modules used here -- sys is a very standard one
import argparse

from libtbngsetup import *

# Gather our code in a main() function
def main(args, loglevel):

  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
  logging.debug("Arguments passed: {0}".format(args))


  if args.dnsmasq_source not in ["none","apt","yum"]:
    raise Exception("apt,yum,none options for dnsmasq are allowed")

  logging.info("Checking {0} is configured manually".format(args.interface))
  logging.info("Trying to get address of interface {0}".format(args.interface))
  ip_address = check_interface(args.interface)

  if not ip_address:
    raise Exception("Cannot determine interface {0} address. Run ifup {0} and restart the script".format(args.interface))

  if args.dnsmasq_source in ["apt","yum"]:
    logging.info("Installing dnsmasq package")
    if (args.dnsmasq_source == "apt"):
      logging.debug(utility.silently_install_by_apt("dnsmasq").decode("utf-8"))
    elif (args.dnsmasq_source == "yum"):
      logging.debug(utility.silently_install_by_yum("dnsmasq").decode("utf-8"))

  logging.info("Configuring dnsmasq")
  settings = """interface={0}
#Configuration of DNS
server=#
server=8.8.8.8
#Configuration of DNS end
dhcp-option={0},option:dns-server,0.0.0.0
dhcp-option={0},option:router,{4}
dhcp-range={0},{1},{2},{3},12h""".format(args.interface,args.dhcpbegin,args.dhcpend,args.dhcpmask,ip_address)
  utility.removeFileData("/etc/dnsmasq.conf",prefix,"dnsmasq settings")
  utility.appendFileData("/etc/dnsmasq.conf",prefix,"dnsmasq settings",settings)
  logging.debug(utility.run_multi_shell_command("systemctl restart dnsmasq").decode("utf-8"))

  logging.debug(utility.run_shell_command("sync").decode("utf-8"))
  logging.info("Dnsmasq configured.")


# Standard boilerplate to call the main() function to begin
# the program.

if sys.version_info[0] < 3:
  raise Exception("Python 3.x is required.")

if not os.geteuid()==0:
  raise Exception("sudo or root is required.")

if __name__ == '__main__':
  parser = argparse.ArgumentParser( 
                                    description = "Script to configure dnsmasq. Use with caution."
                                  )

  parser.add_argument('-i',
                      '--interface',
                       type=str, help="Interface name (wlan0,wlan1,...)",required=True)

  parser.add_argument('-s',
                      '--dnsmasq_source',
                       type=str, default="none",required=True,help="Install dnsmasq from repository. Possible values are apt (install from apt),yum (install from yum) or none (assumed it is installed manually)")
  
  parser.add_argument('-b',
                      '--dhcpbegin',
                       type=str, default="none",required=True, help="DHCP start address, used to configure dnsmasq service. Not validated!")

  parser.add_argument('-e',
                      '--dhcpend',
                       type=str, default="none",required=True, help="DHCP end address, used to configure dnsmasq service. Not validated!")
  
  parser.add_argument('-m',
                      '--dhcpmask',
                       type=str, default="none",required=True, help="DHCP mask, used to configure dnsmasq service. Not validated!")                       
 
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

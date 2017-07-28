#!/usr/bin/env python3
#

# import modules used here -- sys is a very standard one
import sys,argparse,logging,os,json,subprocess
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = Path(current_dir).parent

sys.path.insert(0,'{0}/engine'.format(project_dir))
from libraries import utility

# Gather our code in a main() function
def main(args, loglevel):
  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
  logging.debug("Arguments passed: user {0}, tor config file {1}, privoxy config file {2}".format(args.user,args.torrc,args.privoxyconf))

  logging.info("Checking user {0}".format(args.user))

  logging.info("Configuring tor")

  logging.info("Configuring privoxy")
  
  logging.info("Downloading i2p")

  logging.info("Installing i2p")

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

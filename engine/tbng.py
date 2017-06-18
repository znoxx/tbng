#!/usr/bin/env python3
#

# import modules used here -- sys is a very standard one
import sys, argparse, logging, os, utility,json
from string import Template

configuration=None

# Gather our code in a main() function
def main(args, loglevel):
  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

  #Getting path for config usage
  current_dir = os.path.dirname(os.path.abspath(__file__))

  # TODO
  # Parse config file here 
  config_path = current_dir+"/../config/tbng.json"
  with open(config_path) as data_file:    
    configuration = json.load(data_file)
 
 
  
  # Actual code starts here
  logging.info("We are running in %s" % current_dir)
  logging.debug("Your Command: %s" % args.command)
  logging.debug("Options are: %s" % args.options)

  choices = {
   'masquerade': masquerade, #do not use ()
   'clean_firewall': clean_fw, #do not use ()
   'unknown': unknown, #do not use ()
  }
  
  runfunc = choices[args.command] if choices.get(args.command) else unknown
  runfunc(args.options)  

#function implementation goes here
def unknown(options):
 print("Unknown value passed")

def masquerade(options):
  print("Masquerading called")

def clean_fw(options):
  print("Clean firewall called")
  command_template = Template("""echo "$iptables This is the first string"
                                 echo "$iptables The second"
                                 echo "$iptables The third..." """)
  command=command_template.substitute(iptables=configuration["iptables"])
  utility.run_shell_command(command) 
  #subprocess.check_output(command, shell=True)

   
 
# Standard boilerplate to call the main() function to begin
# the program.

if sys.version_info[0] < 3:
    raise Exception("Python 3.6 or a more recent version is required.")

if sys.version_info[1] < 6:
    raise Exception("Python 3.6 or a more recent version is required.")

if __name__ == '__main__':
  parser = argparse.ArgumentParser( 
                                    description = "Commands executor for TBNG project.",
                                    epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
                                    fromfile_prefix_chars = '@' )

  parser.add_argument(
                      "command",
                      help = "pass command to the program",
                      metavar = "command")

  parser.add_argument(
                      "options",
                      help = "pass command options to the program (optional)",
                      metavar = "options",
                      nargs = '*',
                      default = [])

 
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
  # loading configuration

  
  main(args, loglevel)
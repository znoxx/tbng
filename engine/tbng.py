#!/usr/bin/env python3
#

# import modules used here -- sys is a very standard one
import sys, argparse, logging, os, utility

# Gather our code in a main() function
def main(args, loglevel):
  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

  #Getting path for config usage
  current_dir = os.path.dirname(os.path.abspath(__file__))
  
  # TODO Replace this with your actual code.
  print ("We are running in %s" % current_dir)
  logging.info("You passed an argument.")
  logging.debug("Your Argument: %s" % args.argument)

  choices = {
   'masquerade': masquerade, #do not use ()
   'unknown': unknown, #do not use ()
  }
  
  runfunc = choices[args.argument] if choices.get(args.argument) else unknown
  runfunc()  

#function implementation goes here
def unknown():
 print("Unknown value passed")

def masquerade():
  print("Masquerading called")

 
# Standard boilerplate to call the main() function to begin
# the program.

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

if __name__ == '__main__':
  parser = argparse.ArgumentParser( 
                                    description = "Commands executor for TBNG project.",
                                    epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
                                    fromfile_prefix_chars = '@' )
  # TODO Specify your real parameters here.
  parser.add_argument(
                      "argument",
                      help = "pass ARG to the program",
                      metavar = "ARG")
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
  
  main(args, loglevel)
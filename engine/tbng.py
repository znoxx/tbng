#!/usr/bin/env python3
#


# import modules used here -- sys is a very standard one
import sys, argparse, logging, os, utility,json
from string import Template

configuration=None

# Gather our code in a main() function
def main(args, loglevel):
  global configuration

  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

  #Getting path for config usage
  current_dir = os.path.dirname(os.path.abspath(__file__))

  # TODO
  # Parse config file here 
  config_path = current_dir+"/../config/tbng.json"
  with open(config_path) as data_file:    
    configuration = json.load(data_file)
 
  logging.debug("Configuration loaded from file %s" % config_path)
  logging.debug("Configuration  dump: %s" % configuration)
  # Actual code starts here
  logging.debug("We are running in %s" % current_dir)
  logging.debug("Your Command: %s" % args.command)
  logging.debug("Options are: %s" % args.options)

  print ("is wireless") if is_wireless(configuration['wan_interface'],"wlan0") else print("is not wireless")
  
  choices = {   #do not use ()
   'chkconfig': chkconfig,   # checks config
   'masquerade': masquerade, # enables masquerading on all outbound interfaces
   'clean_firewall': clean_fw, # cleans firewall
   'mode': mode, # sets mode -direct,tor,privoxy
   'unknown': unknown, # stub for unknown option
  }
  
  runfunc = choices[args.command] if choices.get(args.command) else unknown
  runfunc(args.options)  
  
#options checker

def check_options(options,num):
  if num!=len(options):
    raise Exception("Illegal number of options, required number is %d" % num)  

#function implementation goes here
def unknown(options):
 raise Exception("Unknown options passed")

def chkconfig(options):
  check_options(options,0)
  logging.info("Check config called")

def masquerade(options):
  check_options(options,0)
  # template
  tmplScript=""
  # Making list of wan interfaces

  for interface in configuration['wan_interface']:
    tmplScript = tmplScript + "$iptables --table nat --append POSTROUTING --out-interface %s -j MASQUERADE\n" % interface['name'] 
  
  for interface in configuration['lan_interface']:
    tmplScript = tmplScript + "$iptables --append FORWARD --in-interface %s -j ACCEPT\n" % interface['name'] 

  tmplScript = tmplScript + "$iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT\n" 
  tmplScript = tmplScript + "sysctl -w net.ipv4.ip_forward=1\n"

  command_template = Template(tmplScript)
  command = command_template.substitute(iptables=configuration["iptables"])

  logging.debug(utility.run_multi_shell_command(command).decode("utf-8"))
  logging.info("Masquerading called")

def clean_fw(options):
  check_options(options,0)
  command_template = Template("""$iptables -F
                                 $iptables -X
                                 $iptables -t nat -F
                                 $iptables -t nat -X
                                 $iptables -t mangle -F
                                 $iptables -t mangle -X
                                 $iptables -t raw -F
                                 $iptables -t raw -X
                                 $iptables -P INPUT ACCEPT
                                 $iptables -P FORWARD ACCEPT
                                 $iptables -P OUTPUT ACCEPT """)

  command=command_template.substitute(iptables=configuration["iptables"])
  logging.debug(utility.run_multi_shell_command(command).decode("utf-8"))
  logging.info("Clean firewall called")

def mode(options):
  check_options(options,1)
  # TODO: implement mode setting
  if options[0] not in  ['direct','tor','privoxy']:
    raise Exception("Illegal mode")
  
  clean_fw([])
  masquerade([])

  commandTemplate=""
  for interface in configuration['lan_interface']:
   commandTemplate = "$iptables -t nat -A PREROUTING -i %s -p udp --dport 53 -j REDIRECT --to-ports 9053\n" % interface['name']  
   commandTemplate = commandTemplate + "$iptables -t nat -A PREROUTING -i %s -p tcp --syn -j REDIRECT --to-ports 9040\n" % interface['name']

  if options[0] == 'privoxy':
    for interface in configuration['lan_interface']:
      commandTemplate = commandTemplate + "$iptables -t nat -A PREROUTING -i %s -p tcp --dport 80 -j REDIRECT --to-port 8118\n" % interface['name']

  command_template = Template(commandTemplate)
  command = command_template.substitute(iptables=configuration["iptables"])
  
  if options[0] in ['tor','privoxy']:
    logging.debug(utility.run_multi_shell_command(command).decode("utf-8"))
    

  logging.info("Mode setting called")  

def is_wireless(section,name):
  interface_found=False
  for interface in section:
    if interface['name']==name:
      interface_found=True                         
      if 'wireless' in interface and interface['wireless']:
        return True
  if not interface_found:
    raise Exception("Interface not found.")
  return False   
 
# Standard boilerplate to call the main() function to begin
# the program.

if sys.version_info[0] < 3:
    raise Exception("Python 3.x is required.")

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

  
  main(args, loglevel)
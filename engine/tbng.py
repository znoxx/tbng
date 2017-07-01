#!/usr/bin/env python3
#


# import modules used here -- sys is a very standard one
import sys, argparse, logging, os, utility,json
from string import Template

#Getting path for config usage

current_dir = os.path.dirname(os.path.abspath(__file__))
configuration = None
config_path = current_dir+"/../config/tbng.json"
runtime= {}
runtime_path = current_dir+"/../config/runtime.json"

# Gather our code in a main() function
def main(args, loglevel):
  global configuration
  global runtime
  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

  with open(config_path) as data_file:    
    configuration = json.load(data_file)
  logging.debug("Configuration loaded from file {0}".format(config_path))

    
  if os.path.isfile(runtime_path):
    with open(runtime_path) as data_file:    
      runtime = json.load(data_file)
    logging.debug("Runtime data loaded from file {0}".format(runtime_path))
  else:
    ### default runtime is here
    runtime['mode']="direct"
    logging.debug("Runtime not found, creating default")
    update_runtime()
   
  logging.debug("Configuration dump: {0}".format(configuration))
  logging.debug("Runtime dump: {0}".format(runtime))
  # Actual code starts here
  logging.debug("We are running in {0}".format(current_dir))
  logging.debug("Your Command: {0}".format(args.command))
  logging.debug("Options are: {0}".format(args.options))
  
  choices = {   #do not use ()
   'chkconfig': chkconfig,   # checks config
   'masquerade': masquerade, # enables masquerading on all outbound interfaces
   'clean_firewall': clean_fw, # cleans firewall
   'mode': mode, # sets mode -direct,tor,privoxy, restore
   'reboot': reboot, #reboots
   'shutdown': shutdown, #shutdowns
   'tor_restart': tor_restart, #restarts tor
   'i2p_restart': i2p_restart, #(re)starts i2p
   'i2p_stop': i2p_stop, #stops i2p
   'unknown': unknown, # stub for unknown option
  }
  
  runfunc = choices[args.command] if choices.get(args.command) else unknown
  runfunc(args.options)  
  
#options checker

def check_options(options,num):
  if num!=len(options):
    raise Exception("Illegal number of options, required number is {0}".format(num))  

#function implementation goes here
def unknown(options):
 raise Exception("Unknown options passed")

def chkconfig(options):
  check_options(options,0)
  ##getting interface list
  iface_list = os.listdir("/sys/class/net")
  logging.debug("Interface list: {0}".format(iface_list))
  ##checking WAN interfaces
  wireless=0
  wired=0

  if ('wan_interface' not in configuration.keys()) or (not configuration['wan_interface']):
   raise Exception("No WAN interfaces configured")
     
  for interface in configuration['wan_interface']:
    if interface['name'] not in iface_list:
      raise Exception("WAN interface {0} is not defined or does not exist in /sys/class/net".format(interface['name']))
    else: 
      if is_wireless(configuration['wan_interface'],interface['name']):
        wireless +=1
      else:
        wired +=1

  if ( wireless > 1 ) or ( wired > 1 ):
    raise Exception("Only one interface of same type is allowed - wired or wireless")

  #checking LAN Interfaces
  if ('lan_interface' not in configuration.keys()) or (not configuration['lan_interface']):
   raise Exception("No LAN interface configured")

  for interface in configuration['lan_interface']:
    if interface['name'] not in iface_list:
      raise Exception("LAN interface {0} is not defined or does not exist in /sys/class/net".format(interface['name']))
  
  #Checking interface conflicts
  lans=[]
  for interface in configuration['lan_interface']:
    lans.append(interface['name'])
  wans=[]
  for interface in configuration['wan_interface']:
    wans.append(interface['name'])

  if len(set(lans).intersection(wans)) > 0:
   raise Exception("Conflicting interfaces in LAN and WAN are detected: {0}".format(set(lans).intersection(wans)))
 

  logging.info("Check config called")

def masquerade(options):
  check_options(options,0)
  # template
  tmplScript=""
  # Making list of wan interfaces

  for interface in configuration['wan_interface']:
    tmplScript = tmplScript + "$iptables --table nat --append POSTROUTING --out-interface {0} -j MASQUERADE\n".format(interface['name']) 
  
  for interface in configuration['lan_interface']:
    tmplScript = tmplScript + "$iptables --append FORWARD --in-interface {0} -j ACCEPT\n".format(interface['name']) 

  tmplScript = tmplScript + "$iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT\n" 
  tmplScript = tmplScript + "sysctl -w net.ipv4.ip_forward=1\n"

  logging.debug(utility.run_multi_shell_command(Template(tmplScript).substitute(iptables=configuration["iptables"])).decode("utf-8"))
  logging.info("Masquerading called")

def clean_fw(options):
  check_options(options,0)
  logging.debug(utility.run_multi_shell_command(Template("""$iptables -F
  $iptables -X
  $iptables -t nat -F
  $iptables -t nat -X
  $iptables -t mangle -F
  $iptables -t mangle -X
  $iptables -t raw -F
  $iptables -t raw -X
  $iptables -P INPUT ACCEPT
  $iptables -P FORWARD ACCEPT
  $iptables -P OUTPUT ACCEPT""").substitute(iptables=configuration["iptables"])).decode("utf-8"))
  logging.info("Clean firewall called")

def mode(options):
  check_options(options,1)
  
  if options[0] not in  ['direct','tor','privoxy','restore']:
    raise Exception("Illegal mode")
  

  commandModeTemplate=""
  for interface in configuration['lan_interface']:
   commandModeTemplate = "$iptables -t nat -A PREROUTING -i {0} -p udp --dport 53 -j REDIRECT --to-ports 9053\n".format(interface['name'])  
   commandModeTemplate = commandModeTemplate + "$iptables -t nat -A PREROUTING -i {0} -p tcp --syn -j REDIRECT --to-ports 9040\n".format(interface['name'])

  if options[0] == 'restore':
    options[0] = runtime['mode']

  if options[0] == 'privoxy':
    for interface in configuration['lan_interface']:
      commandModeTemplate = commandModeTemplate + "$iptables -t nat -A PREROUTING -i {0} -p tcp --dport 80 -j REDIRECT --to-port 8118\n".format(interface['name'])
  
  clean_fw([])

  #Allowing desired ports
  allowed_ports = [22,3000,7657,9050,8118] + configuration['allowed_ports']
  
  commandAllowTemplate="sysctl -w net.ipv4.ip_forward=1\n" #must run always
  for interface in configuration['lan_interface']:
    for port in allowed_ports:
      commandAllowTemplate = commandAllowTemplate + "$iptables -t nat -A PREROUTING -i {0} -p tcp --dport {1} -j REDIRECT --to-port {2}\n".format(interface['name'],port,port)  
  logging.debug(utility.run_multi_shell_command(Template(commandAllowTemplate).substitute(iptables=configuration["iptables"])).decode("utf-8"))

  if options[0] in ['tor','privoxy']:
    logging.debug(utility.run_multi_shell_command(Template(commandModeTemplate).substitute(iptables=configuration["iptables"])).decode("utf-8"))
  else:
    masquerade([])

  #Locking firewall if needed
  commandLockTemplate = "$iptables  -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT\n"
  for interface in configuration['wan_interface']:
   commandLockTemplate = commandLockTemplate + "$iptables -A INPUT -i {0} -j DROP\n".format(interface['name'])
  
  if configuration['lock_firewall']:
    logging.debug(utility.run_multi_shell_command(Template(commandLockTemplate).substitute(iptables=configuration["iptables"])).decode("utf-8"))
  
  runtime['mode']=options[0]
  update_runtime()

  logging.info("Mode setting called - mode {0} selected".format(options[0]))  

def reboot(options):
  check_options(options,0)
  logging.debug(utility.run_shell_command("reboot").decode("utf-8"))

def shutdown(options):
  check_options(options,0)
  logging.debug(utility.run_shell_command("shutdown -h now").decode("utf-8"))

def tor_restart(options):
  check_options(options,0)
  logging.debug(utility.run_shell_command("systemctl restart tor").decode("utf-8"))

def i2p_restart(options):
  check_options(options,0)
  logging.debug(utility.run_shell_command("systemctl restart i2p-torbox").decode("utf-8"))

def i2p_stop(options):
  check_options(options,0)
  logging.debug(utility.run_shell_command("systemctl stop i2p-torbox").decode("utf-8"))


def is_wireless(section,name):
  interface_found=False
  logging.debug("is_wireless called with section: {0} and name: {1}".format(section,name)) 
  for interface in section:
    if interface['name']==name:
      interface_found=True                         
      if 'wireless' in interface and interface['wireless']:
        return True
  if not interface_found:
    raise Exception("Interface not found.")
  return False   

def update_runtime():
  with open(runtime_path, 'w') as outfile:
    json.dump(runtime, outfile)
  logging.debug("Runtime updated at {0}".format(runtime_path))
 
# Standard boilerplate to call the main() function to begin
# the program.

if sys.version_info[0] < 3:
    raise Exception("Python 3.x is required.")

if not os.geteuid()==0:
 raise Exception("sudo or root is required.")

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

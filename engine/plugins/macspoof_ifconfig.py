## Using arguments
from libraries import utility
import json
def plugin_main(json_arguments=None):
  if json_arguments is not None:
    interface=json.loads(json_arguments)
    if ('name' not in interface.keys()) or (not interface['name']):
      raise Exception("No interface name passed")
    command="""ip link set {0} down
    macaddr=$(printf '%02x' $((0x$(od /dev/urandom -N1 -t x1 -An | cut -c 2-) & 0xFE | 0x02)); od /dev/urandom -N5 -t x1 -An | sed 's/ /:/g')
    ifconfig {0} hw ether $macaddr
    ip link set {0} up
    """.format(interface['name'])
    utility.run_multi_shell_command(command)
  else:
   raise Exception("Arguments for this plugin are  mandatory")

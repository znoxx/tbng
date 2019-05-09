## Spoofing mac via realtek module reload
from libraries import utility
import json
def plugin_main(json_arguments=None):
  if json_arguments is not None:
    interface=json.loads(json_arguments)
    if ('name' not in interface.keys()) or (not interface['name']):
      raise Exception("No interface name passed")
    if ('module_name' not in interface.keys()) or (not interface['module_name']):
      raise Exception("No module name passed")
    command="""ip link set {0} down
    macaddr=$(printf '%02x' $((0x$(od /dev/urandom -N1 -t x1 -An | cut -c 2-) & 0xFE | 0x02)); od /dev/urandom -N5 -t x1 -An | sed 's/ /:/g')
    rmmod {1}
    modprobe {1} rtw_power_mgnt=0 rtw_enusbss=0 rtw_initmac=${{macaddr}}
    sleep 3
    ip link set {0} up
    systemctl restart network-manager
    """.format(interface['name'],interface['module_name'])
    utility.run_multi_shell_command(command)
  else:
   raise Exception("Arguments for this plugin are  mandatory")

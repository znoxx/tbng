## Spoofing mac via macchanger on ug802 with broadcom chipset
from libraries import utility
import json
def plugin_main(json_arguments=None):
  if json_arguments is not None:
    interface=json.loads(json_arguments)
    if ('name' not in interface.keys()) or (not interface['name']):
      raise Exception("No interface name passed")
    command="""/usr/bin/macchanger -A {0} || true
    systemctl restart network-manager.service
    sleep 5
    """.format(interface['name'])
    utility.run_multi_shell_command(command)
  else:
   raise Exception("Arguments for this plugin are  mandatory")

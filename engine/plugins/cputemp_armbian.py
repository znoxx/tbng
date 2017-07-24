## Armbian plugin for temperature measurment
from libraries import utility
def plugin_main(json_arguments=None):
  data="Undefned"  
  with open ("/sys/class/hwmon/hwmon1/temp1_input", "r") as temperature:
    data=temperature.read()
  return "{0} C".format(int(data))

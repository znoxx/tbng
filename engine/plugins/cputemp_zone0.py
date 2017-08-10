## Armbian plugin for temperature measurment
from libraries import utility
def plugin_main(json_arguments=None):
  data="Undefned"  
  with open ("/sys/class/thermal/thermal_zone0/temp", "r") as temperature:
    data=temperature.read()
  return "{0} C".format(int(data)/1000)

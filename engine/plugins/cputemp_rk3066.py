## RK3066 plugin for temperature measurment
from libraries import utility
def plugin_main(json_arguments=None):
  kernel0="Undefned"  
  kernel1="Undefined"
  with open ("/sys/module/tsadc/parameters/temp0", "r") as temperature:
    kernel0=temperature.read()
  with open ("/sys/module/tsadc/parameters/temp1", "r") as temperature:
    kernel1=temperature.read()  
  return "CPU0:{0} CPU1:{1} C".format(kernel0.split(" ")[1],kernel1.split(" ")[1])

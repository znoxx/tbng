
def plugin_main():
  data="Undefned"  
  with open ("/sys/class/thermal/thermal_zone0/temp", "r") as temperature:
    data=temperature.read()
  return "{0} C".format(int(data)/1000)
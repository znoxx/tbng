def plugin_main():
  data="Undefned"  
  with open ("/sys/class/hwmon/hwmon0/device/temp1_input", "r") as temperature:
    data=temperature.read()
  return "{0} C".format(int(data)/1000)

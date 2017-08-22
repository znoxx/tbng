## RPI1 plugin for temperature 
import subprocess
from libraries import utility
def plugin_main(json_arguments=None):
  data="Undefned"
  data=subprocess.check_output(['/opt/vc/bin/vcgencmd', 'measure_temp']).decode('utf-8')  
  return "{0}".format(data.replace("temp=","").replace("'"," ").rstrip())


import argparse, sys
from libraries.plugin_loader import run_plugin

if sys.version_info[0] < 3:
    raise Exception("Python 3.x is required.")

parser = argparse.ArgumentParser()
parser.add_argument("plugin_family", help="Sets plugin family (cputemp/macspoof)")
parser.add_argument("plugin_name", help="Set plugin name")
args = parser.parse_args()

plugin_family=args.plugin_family
plugin_name=args.plugin_name

print("Running plugin from plugin/{0}_{1}.py".format(plugin_family,plugin_name))

return_value=run_plugin(plugin_family,plugin_name)

print("Return value: {0}".format(return_value))
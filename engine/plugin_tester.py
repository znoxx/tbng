#!/usr/bin/env python3


import argparse, sys
from libraries.plugin_loader import run_plugin

if sys.version_info[0] < 3:
    raise Exception("Python 3.x is required.")

parser = argparse.ArgumentParser()
parser.add_argument("plugin_family", help="Sets plugin family (cputemp/macspoof)")
parser.add_argument("plugin_name", help="Set plugin name")
parser.add_argument('plugin_parameter', nargs='?', default=None)
args = parser.parse_args()

plugin_family=args.plugin_family
plugin_name=args.plugin_name
plugin_parameter=args.plugin_parameter

print("Running plugin from plugin/{0}_{1}.py with parameter {2}".format(plugin_family,plugin_name, plugin_parameter))

return_value=run_plugin(plugin_family,plugin_name,plugin_parameter)

print("Return value: {0}".format(return_value))

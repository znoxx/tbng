from importlib import import_module
def run_plugin(family,name,json_arguments=None):
    return_value="Error getting data for plugin/{0}_{1}.py: ".format(family,name)
    try:
      plugin = import_module("plugins.{0}_{1}".format(family,name))
      return_value=plugin.plugin_main(json_arguments)
    except Exception as e:
      return_value += str(e)
      raise Exception(return_value)
    return return_value

from importlib import import_module
def run_plugin(family,name):
    plugin = import_module("plugins.{0}_{1}".format(family,name))
    return_value="Error getting data plugin/{0}_{1}.py: ".format(family,name)
    try:
      return_value=plugin.plugin_main()
    except Exception as e:
      return_value += str(e)
    return return_value
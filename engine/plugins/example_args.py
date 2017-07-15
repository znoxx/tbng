## Using arguments
def plugin_main(json_arguments=None):
  if json_arguments is not None:
   return "Parameter passed: {0}".format(json_arguments)
  else:
   return "I was called without params"

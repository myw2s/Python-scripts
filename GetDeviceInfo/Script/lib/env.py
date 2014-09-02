from com.atmel.wsnrunner import PyEnvironment
import misc

#********************************************************************************
# Get values from config with specified prefix
#
# Parameters:
#   prefix - prefix to look for
#
# Return:
#   Dict of values with specified prefix.
#
#********************************************************************************
def getByPrefix(prefix):
  return misc.filterByPrefix(PyEnvironment.getEnvironment(), prefix)

#********************************************************************************
# Get build parameters for stack, HAL and applications.
#
# Parameters:
#   none
#
# Return:
#   Dict of raw build parameters for stack, HAL and applications.
#
#********************************************************************************
def getOptions():
  env = PyEnvironment.getEnvironment()
  res = {}
  for k, v in env.iteritems():
    if k.startswith('stack.') or k.startswith('hal.') or k.startswith('app.'):
      res[k] = v.strip()
  return res

#********************************************************************************
# Get list of variables from config.
#
# Parameters:
#   none
#
# Return:
#   Dict with variables from config.
#
#********************************************************************************
def getVariables():
  return misc.filterByPrefix(PyEnvironment.getEnvironment(), 'var')

#********************************************************************************
# Get command line parameters.
#
# Parameters:
#   none
#
# Return:
#   List with command line parameters.
#
#********************************************************************************
def getCommandLine():
  return PyEnvironment.getEnvironment()['commandLine']

#********************************************************************************
# Get value of parameter from config.
#
# Parameters:
#   param - parameter which name is needed
#
# Return:
#   Value of requested parameter or None if parameter is not found.
#
#********************************************************************************
def getValue(param):
  env = PyEnvironment.getEnvironment()
  if param in env:
    return env[param].strip()
  else:
    return None

#********************************************************************************
# Get list of nodes from config file.
#
# Parameters:
#   amount - amount of nodes to get
#   respectLimit - limit amount of nodes returned to value of 'nodesLimit'
#     parameter from config
#
# Return:
#   List of nodes from config file and server.
#
#********************************************************************************
def getNodeList(amount, respectLimit=False, sampleApp=False):
  if sampleApp:
    misc.sampleAppNodes = None

  nodeList = getValue('nodes')
  nodesLimit = getValue('nodesLimit')
  if nodesLimit:
    nodesLimit = eval(nodesLimit)

  nodes = []
  if nodeList:
    for node in nodeList.split(','):
      node = node.strip()
      if node.startswith('COM') or not misc.__client:
        nodes += [node]

  if misc.__client:
    need = amount - len(nodes)

    if respectLimit and nodesLimit:
      if len(nodes) < nodesLimit:
        need = min(need, nodesLimit - len(nodes))
        nodes += misc.__client.getNodes(need)
      else:
        nodes = nodes[0:nodesLimit]
    else:
      if need > 0:
        nodes += misc.__client.getNodes(need)
      else:
        nodes = nodes[0:amount]

  if sampleApp:
    misc.sampleAppNodes = nodes

  return nodes

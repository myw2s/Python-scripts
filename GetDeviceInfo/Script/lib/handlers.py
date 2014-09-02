import sys

import env
import misc
import cache
import nodes

from public import *

#********************************************************************************
# Chech for presence of commonly required parameters in config file.
#
# Parameters:
#   none
#
# Return:
#   True - all required parameters are present
#   False - some of required parameters are not present or invalid
#
#********************************************************************************
def checkConfigFile():
  return True

  # Check that all mandatory parameters are present in config file
  for path in ['stackPath', 'halPath', 'appPath']:
    value = env.getValue(path)
    if value is None:
      log.error('Fatal error: "%s" parameter not found in config file' % path, log = 'tester')
      return False
  return True

#********************************************************************************
# 'sampleapptest' script handler.
#
# Parameters:
#   name - name of script
#   info - description from script
#
# Return:
#   none
#
#********************************************************************************
def h_sampleapptest(name, info):
  if checkConfigFile():
    misc.sampleAppTestFailed = False
    log.openSampleAppLog(name)
    cache.init()
    variables = globals().copy()
    execfile(misc.expandPath(name), variables, variables)
    cache.cleanup()
    log.closeSampleAppLog()

#********************************************************************************
# 'sampleapp' script handler.
#
# Parameters:
#   name - name of script
#   info - description from script
#
# Return:
#   none
#
#********************************************************************************
def h_sampleapp(name, info):
  log.error('%s: can not execute standalone sample application test' % name, log = 'tester')

#********************************************************************************
# 'testcase' script handler.
#
# Parameters:
#   name - name of script
#   info - description from script
#
# Return:
#   none
#
#********************************************************************************
def h_testcase(name, info):
  variables = misc.evalValues(misc.cdicts(env.getVariables(), info['variables']))
  nodesList = env.getNodeList(10000)
  nodes.setStatus(nodesList, name)
  testerMode = misc.runOnOptions[info['runon']]['tester']

  for portName, connParameters in info['conns'].iteritems():
    type, port, conf = connParameters
    if port:
      if port.startswith('IDX'):
        try:
          index = int(port.split(':')[1].strip())
          connName = nodesList[index]
        except:
          log.error('Incorrect index for port', log = "tester")
          return
      else:
        connName = port
    else:
      if len(nodesList) > 0:
        connName = nodesList[0]
        nodesList = nodesList[1:]
      else:
        log.error('Not enough nodes', log = "tester")
        return
    nodes.restart([misc.__nodeFactory.create(connName),]) #power on node
    log.write('Using %s for %s' % (connName, portName), log = "tester")
    variables[portName] = misc.__nodeFactory.create(connName).getConnection()
    #variables[portName].setTesterMode(testerMode)

  vars = globals().copy()
  
  vars.update(variables)
  if '.py' != name[-len('.py'):]:
    vars['scriptPath'] = misc.expandPath(name)[:-len(name + '.py')]
  else:
    vars['scriptPath'] = misc.expandPath(name)[:-len(name)]

  sys.path.append(vars['scriptPath'])
  execfile(misc.expandPath(name), vars, vars)
  log.write('SUCCESS', log = "tester")

#********************************************************************************
# 'testsuite' script handler.
#
# Parameters:
#   name - name of script
#   info - description from script
#
# Return:
#   none
#
#********************************************************************************
def h_testsuite(name, info):
  misc.testSuiteName = name
  misc.runOn = misc.runOnOptions[info['runon']]

  if checkConfigFile():
    vars = globals().copy()
    if '.py' != name[-len('.py'):]:
      vars['scriptPath'] = misc.expandPath(name)[:-len(name + '.py')]
    else:
      vars['scriptPath'] = misc.expandPath(name)[:-len(name)]
    sys.path.append(vars['scriptPath'])
    execfile(misc.expandPath(name), vars, vars)

#********************************************************************************
# 'function' script handler.
#
# Parameters:
#   name - name of script
#   info - description from script
#
# Return:
#   none
#
#********************************************************************************
def h_function(name, info):
  log.error('%s: can not execute standalone function' % name, log = 'tester')

#********************************************************************************
# 'rawfile' script handler.
#
# Parameters:
#   name - name of script
#   info - description from script
#
# Return:
#   none
#
#********************************************************************************
def h_rawfile(name, info):
  try:
    vars = globals().copy()
    if '.py' != name[-len('.py'):]:
      vars['scriptPath'] = misc.expandPath(name)[:-len(name + '.py')]
    else:
      vars['scriptPath'] = misc.expandPath(name)[:-len(name)]
    sys.path.append(vars['scriptPath'])
    execfile(misc.expandPath(name), vars, vars)
  except SystemExit:
    pass

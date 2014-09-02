import time
from com.atmel.wsnrunner import LogFactory
from com.atmel.wsnrunner import TesterException
from com.atmel.wsnlibrary import RunInfo
import exc
import env
import log
import misc
import cache
import nodes

#********************************************************************************
# Run list of cases.
#
# Parameters:
#   caseList - dict with case name as a key and list of build_parameters-variables
#     combinations as a value
#
# Return:
#   none
#
#********************************************************************************
def runTestCases(caseList):
  import testSuite
  testSuite.runTestCases(caseList)

#********************************************************************************
# Open log file.
#
# Parameters:
#   fileName - log file name
#   log - internal name of log (used by writeLog() and co)
#   enableConsole - enable console output for this log
#
# Return:
#   none
#
#********************************************************************************
def openLog(fileName, logName = 'testcase', enableConsole=False):
  log.open(fileName, logName, enableConsole)

#********************************************************************************
# Open log with file name format specific for sample applications test.
#
# Parameters:
#   name - base for file name
#
# Return:
#   none
#
#********************************************************************************
def openSampleAppLog(name):
  log.openSampleAppLog(name)

#********************************************************************************
# Close log opened by openSampleAppLog().
#
# Parameters:
#   none
#
# Return:
#   none
#
#********************************************************************************
def closeSampleAppLog():
  log.closeSampleAppLog()

#********************************************************************************
# Output string to log with "info" level.
#
# Parameters:
#   msg - string to write
#   log - internal name of log
#
# Return:
#   none
#
#********************************************************************************
def writeLog(msg, logName = 'testcase'):
  log.write(msg, logName)

#********************************************************************************
# Output string to log with "error" level.
#
# Parameters:
#   msg - string to write
#   log - internal name of log
#
# Return:
#   none
#
#********************************************************************************
def errorLog(msg, logName = 'testcase'):
  log.error(msg, logName)

#********************************************************************************
# Get version and build number of environment we are running on.
#
# Parameters:
#   none
#
# Return:
#   Tuple containing version and build number.
#
#********************************************************************************
def envVersion():
  return (str(RunInfo.get().getAppVersion()),
    str(RunInfo.get().getAppBuildNumber()))

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
def envGetCommandLine():
  return env.getCommandLine()

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
def envGetNodeList(amount, respectLimit=False, sampleApp=False):
  return env.getNodeList(amount, respectLimit, sampleApp)

#********************************************************************************
# Check condition. Can be used anywhere inside scripts.
#
# Parameters:
#   condition - condition to check
#
# Return:
#   none
#
#********************************************************************************
def check(condition, logString = None, port = None, logName = 'testcase'):
  if port is None or ((port is not None) and (not port.isDummy())):
    if not condition:
      raise exc.TestFailed(logString, logName)

#********************************************************************************
# Sleep for specified amount of time.
#
# Parameters:
#   seconds - number of seconds to sleep (can be non-integer value to delay for
#     fractions of second)
#
# Return:
#   none
#
#********************************************************************************
def sleep(seconds):
    writeLog('Sleeping for %d seconds' % seconds)
    time.sleep(seconds)

#********************************************************************************
# Call to a function. Function should store its return values in local variable
# named 'ret'. 'ret' should be of dict type.
#
# Parameters:
#   name - function name
#   values - any variables to be passed to the function
#
# Return:
#   Function return values
#
#********************************************************************************
def function(name, **values):
  misc.__stateManager.functionBegin(name,values);
  values['ret'] = {}

  if '__silent' not in values:
    log.write('%s {' % name)
    LogFactory.incPrefix('system')

  variables = globals().copy()
  variables.update(values)

  try:
    execfile(misc.expandPath(name), variables, variables)
  except exc.FReturn, exception:
    ret = exception.getReturnValue()
    if ret:
      variables['ret'] = ret
  finally:
    misc.__stateManager.functionEnd(name);

  if '__silent' not in values:
    LogFactory.decPrefix('system')
    log.write('}\n')
  return variables['ret']

#********************************************************************************
# Return from function.
#
# Parameters:
#   ret - return value
#
# Return:
#   none
#   none
#
#********************************************************************************
def freturn(ret = None):
  raise exc.FReturn(ret)

#********************************************************************************
# Run sample application test.
#
# Parameters:
#   name - sample application test script name
#   values - any variables to be passed to the test
#
# Return:
#   none
#
#********************************************************************************
def sampleApp(name, **values):
  values['ret'] = {}
  res = True

  fullName = misc.expandPath(name)
  if fullName is None:
    log.error('File not found: %s' % name, log = 'suite')
    misc.sampleAppTestFailed = True
    return values['ret']

  variables = globals().copy()
  variables.update(values)

  try:
    execfile(fullName, variables, variables)
  except exc.TestFailed, exception:
    misc.sampleAppTestFailed = True
    res = False
  except TesterException:
    log.error('TestEnvironment internal error.')
    misc.sampleAppTestFailed = True
    res = False
  except:
    misc.sampleAppTestFailed = True
    res = False
    log.printTraceback()
  return res #variables['ret']

#********************************************************************************
# Select connection with data available on it from specified set of connections.
# Fail if no connection selected in specefied amount of time.
#
# Parameters:
#   connSet - list of connections to select from
#   timeout - time to wait for data (in seconds, can be non-integer)
#
# Return:
#   Connection on which data is available
#
#********************************************************************************
def select(connSet, timeout=15):
  timeout *= 1000
  quantum = 100
  while timeout > 0:
    for port in connSet:
      timeout -= quantum
      if port.available(quantum):
        return port

  check(0) # Select failed

#********************************************************************************
# Start timer and run callback after it fires.
#
# Parameters:
#   timeout - time to wait
#   callback - function to call once timer is fired
#
# Return:
#   Started Timer object
#
#********************************************************************************
def timer(timeout, callback):
  t = Timer(timeout, callback)
  t.start()
  return t

#********************************************************************************
# Build set of images and put them to the cache for later use.
#
# Parameters:
#   prefix - path prefix
#   name - expected resulting file name
#   reqired - list of required image parameters in natural format
#
# Return:
#   Number of images built (or already available in the cache)
#
#********************************************************************************
def buildImages(prefix, name, reqired):
  intReq = reqired[:]
  intReq.sort()
  res = misc.buildRequiredImages(intReq, prefix, name, 'old')
  cache.sync()
  return res

#********************************************************************************
# Separate options from natural (raw) format to tuple containing parameters
# for stack, HAL and application.
#
# Parameters:
#   options - options in natural format
#
# Return:
#   tuple containing parameters for stack, HAL and application.
#
#********************************************************************************
def separateOptions(options):
  stack = misc.evalValues(misc.filterByPrefix(options, 'stack'))
  hal = misc.evalValues(misc.filterByPrefix(options, 'hal'))
  app = misc.evalValues(misc.filterByPrefix(options, 'app'))
  return (stack, hal, app)

#********************************************************************************
# Convert list of integers (ASCII codes) to string.
#
# Parameters:
#   lst - list of ASCII codes
#
# Return:
#   String of characters with ASCII codes from specified list.
#
#********************************************************************************
def listToStr(lst):
  return ''.join([chr(c) for c in lst])

#********************************************************************************
# Convert string to list of integers (ASCII codes).
#
# Parameters:
#   str - string to convert
#
# Return:
#   List of ASCII codes for characters in string.
#
#********************************************************************************
def strToList(str):
  return [ord(c) for c in str]

#********************************************************************************
# Get path to the current working directory.
#
# Parameters:
#   none
#
# Return:
#   Path to the current working directory.
#
#********************************************************************************
def getCWD():
  return RunInfo.get().getWorkFolder()

#********************************************************************************
# Request arbitrary node from resource manager.
#
# Parameters:
#   addr - node address
#
# Return:
#   True - node is availabe and reserved
#   False - node is not available
#
#********************************************************************************
def requestNode(addr):
  return nodes.requestNode(addr)

#********************************************************************************
# Send satatus of nodes to resource manager.
#
# Parameters:
#   nodesList - list of nodes
#   status - status to send
#
# Return:
#   none
#
#********************************************************************************
def setNodesStatus(nodesList, status):
  nodes.setStatus(nodesList, status)

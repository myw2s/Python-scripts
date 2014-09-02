import sys
import traceback
from com.atmel.wsnrunner import TesterException
from com.atmel.wsnrunner import WSNServicesFactories
import env
import exc
import log
import misc
import handlers
import scriptInfo

#********************************************************************************
# Main function called by the Java part of the environment.
# Entry point to the python part.
#
# Parameters:
#   name - name of the script to execute
#
# Return:
#   none
#
#********************************************************************************
def runTestScript(name):
  # Open the system logger explicitely to prevent direct console messages
  log.open(None, log = 'system', enableConsole = False)
  
  # Open the tester and test case loggers
  log.open(None, log = 'tester', enableConsole = False)
  log.open(None, log = 'testcase', enableConsole = False)
  
  log.write("Running test script " + name, log = 'tester')
  
  misc.__stateManager=__stateManager
  misc.__nodeFactory=__nodeFactory
  server = env.getValue('resourceManagerServer')
  if server:
    factory=WSNServicesFactories.get('com.atmel.wsnrunner.testwsn.TestWSNClientFactory')
    WSNClientObj = factory.create()
    misc.__client = WSNClientObj.create(server)
    if not misc.__client:
      log.error('Can not connect to resource manager server', log = 'tester')
      return
  else:
    misc.__client = None

  if misc.__client:
    misc.__user = env.getValue('user')
    if not misc.__user:
      log.error('Can not determine user name to use', log = 'tester')
      misc.__client.close()
      return

    misc.__password = env.getValue('password')
    if not misc.__password:
      misc.__password=misc.__user

    misc.__sessionId = env.getValue('sessionId')
    if not misc.__sessionId:
      misc.__sessionId=-1

    misc.__client.authenticate(misc.__user,misc.__password,misc.__sessionId)


  commandMode = name == '-i'

  while True:
    if commandMode:
      name = raw_input('\n> ')
      if name == '':
        break

    fullName = misc.expandPath(name)
    if fullName is None:
      log.error('File not found: %s' % name, log = 'tester')
      if commandMode:
        continue
      else:
        break

    try:
      h = {
        'sampleapptest': handlers.h_sampleapptest,
        'sampleapp'    : handlers.h_sampleapp,
        'testcase'     : handlers.h_testcase,
        'testsuite'    : handlers.h_testsuite,
        'function'     : handlers.h_function,
        'rawfile'      : handlers.h_rawfile,
      }

      info = scriptInfo.getScriptInfo(fullName)
      h[info['type']](name, info)

    except scriptInfo.GetScriptInfoError, exception:
      log.error(str(exception), log = 'tester')

    except exc.TestFailed, exception:
      logName = exception.getLogger()
      if logName is None:
        logName = 'tester'
        
      if exception.getMessage() is None:
        tb = traceback.extract_tb(sys.exc_info()[2])
        log.error(misc.formatFailMsg(tb[-2]), log = logName)
      else:
        log.error(str(exception), log = logName)

    except TesterException:
      log.error('TestEnvironment internal error.', log = 'tester')

    except:
      log.printTraceback(log = 'tester')

    if not commandMode:
      break

  if misc.__client:
    misc.__client.close()

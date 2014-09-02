import os
import sys
import traceback
from com.atmel.wsnrunner import LogFactory
from com.atmel.wsnlibrary.syslogger import SysLogger
import env
import misc

#********************************************************************************
# Open log file.
#
# Parameters:
#   fileName - log file name
#   log - internal name of log
#   enableConsole - enable console output for this log
#
# Return:
#   none
#
#********************************************************************************
def open(fileName, log = 'system', enableConsole = True):
  logLevel = env.getValue('logLevel')
  if logLevel == None:
    logLevel = 'info'

  LogFactory.closeLogger(log)

  if fileName:
    l = LogFactory.createLog(log, fileName)
  else:
    # If no filename is given use /dev/null or NUL to prevent console output
    l = LogFactory.createLog(log, 'NUL')

  l.setLevel(logLevel)
  #SysLogger.setLevel(logLevel)

  if enableConsole:
    LogFactory.enableConsole(log)

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
  logPath = env.getValue('logPath')
  if logPath is None:
    logPath = '.'
  logName = os.path.join(logPath, '%s_%s' % (name, misc.getTimeStr()))
  open(logName + '.txt', log = 'suite')
  open(logName + '_full.txt')

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
  error('-' * 40, log = 'suite')
  if misc.sampleAppTestFailed:
    error('Total result: FAIL', log = 'suite')
  else:
    error('Total result: SUCCESS', log = 'suite')

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
def write(msg, log = 'system'):
  LogFactory.createLog(log).info(msg)

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
def error(msg, log = 'system'):
  LogFactory.createLog(log).error(msg)

#********************************************************************************
# Output traceback of python exception to 'system' log.
#
# Parameters:
#   none
#
# Return:
#   none
#
#********************************************************************************
def printTraceback(log = 'system'):
  tb = traceback.extract_tb(sys.exc_info()[2])
  err = str(sys.exc_info()[0]).replace('exceptions.', '')
  msg = sys.exc_info()[1]

  write('Error occured, traceback follows:')
  for record in tb:
    write('  %s, %d: %s' % (record[0], record[1], record[3]))
  error('%s: %s' % (err, msg))

  # This part is needed if logging system could not start and is not functioning
  print '---------------------------------'
  print 'Error occured, traceback follows:'
  for record in tb:
    print '  %s, %d: %s' % (record[0], record[1], record[3])
  print '%s: %s' % (err, msg)

#********************************************************************************
# Output component (stack, hal, app) build parameters.
#
# Parameters:
#   options - dict containing build parameters in natural form
#
# Return:
#   none
#
#********************************************************************************
def printOptions(options):
  for k, v in options.iteritems():
    write('  %s = %s' % (k, v), log = 'suite')

#********************************************************************************
# Output components (stack, hal, app) build parameters.
#
# Parameters:
#   options - dict containing build parameters in separated form
#
# Return:
#   none
#
#********************************************************************************
def printCompressedOptions(options, log = 'system'):
  stack, hal, app = options

  for k, v in stack.iteritems():
    write('    stack.%s = %s' % (k, v), log)

  for k, v in hal.iteritems():
    write('    hal.%s = %s' % (k, v), log)

  for k, v in app.iteritems():
    write('    app.%s = %s' % (k, v), log)


import os
import sys
import time
import tempfile
import threading
from subprocess import Popen, PIPE, STDOUT
from com.atmel.wsnrunner.runner import Settings
import log
import env
import cache
import guess

build = True
upload = True
checkExpectedVariables = False
statisticsFileName = 'statistics.txt'

runOnOptions = {

  'SeApp': {
    'path'  : 'CustomApps/TestSeApp',
    'srec'  : 'TestSeApp.srec',
    'tester': True,
    'style' : 'new',
    'config': 'TestSEApp.cf',
  },

  'stack': {
    'path'  : 'ZAppSi/Runner',
    'srec'  : 'Runner.srec',
    'tester': True,
    'style' : 'new',
    'config': 'Runner_night_build.cf',
  },

  'mac':
  {
    'path'  : 'TestApps/WSNTester/MAC',
    'srec'  : 'MacTester.srec',
    'tester': True,
    'style' : 'new',
    'config': 'MacTester.cf',
  },

  'serialnet': {
    'path'  : 'SerialNet',
    'srec'  : 'sn_std/SerialNet.srec',
    'tester': False,
    'style' : 'old',
  }
}

#********************************************************************************
# Class used by timer() function.
#********************************************************************************
class Timer(threading.Thread):
  def __init__(self, timeout, callback):
    self.__timeout = timeout
    self.__callback = callback
    threading.Thread.__init__(self)

  def stop(self):
    self.__timeout = None

  def run(self):
    quant = 0.1
    while self.__timeout > 0:
      time.sleep(quant)
      if self.__timeout is None:
        return
      self.__timeout -= quant
    self.__callback()

#********************************************************************************
# Create formatted message with information on check() fail.
#
# Parameters:
#   tb - python traceback information
#
# Return:
#   Formatted string.
#
#********************************************************************************
def formatFailMsg(tb):
  return 'Check failed %s, %d: %s' % (tb[0], tb[1], tb[3])

#********************************************************************************
# Create formatted message with traceback record
#
# Parameters:
#   tb - python traceback information
#
# Return:
#   Formatted string.
#
#********************************************************************************
def formatTraceMsg(rec):
  return '  %s, %d: %s' % (rec[0], rec[1], rec[3])

#********************************************************************************
# Create formatted string with current local time.
#
# Parameters:
#   none
#
# Return:
#   Formatted string.
#
#********************************************************************************
def getTimeStr():
  return time.strftime('%Y_%m_%d__%H_%M_%S', time.localtime())

#********************************************************************************
# Get full file name by short name of script.
#
# Parameters:
#   name - short name of script
#
# Return:
#   Full file name with path.
#
#********************************************************************************
def expandPath(name):
  return Settings.getInstance().getScriptPath(name)

#********************************************************************************
# Concat set of dicts
#
# Parameters:
#   dicts - set of dicts
#
# Return:
#   Dict with information from all specified dicts.
#
#********************************************************************************
def cdicts(*dicts):
  res = {}
  for d in dicts:
    res.update(d)
  return res

#********************************************************************************
# Concat lists
#
# Parameters:
#   lists - set of lists
#
# Return:
#   List containing data from all specified lists.
#
#********************************************************************************
def clists(lists):
  sum = []
  for lst in lists:
    for element in lst:
      while sum.count(element) < lst.count(element):
        sum += [element]
  return sum

#********************************************************************************
# Evaluate values from dict. If eval() failes for some reason value is
# returned as is.
#
# Parameters:
#   values - dict with values to evaluate
#
# Return:
#   Dict with evaluated values
#
#********************************************************************************
def evalValues(values):
  ret = {}
  for k, v in values.iteritems():
    try:
      ret[k] = eval(v)
    except:
      ret[k] = v
  return ret

#********************************************************************************
# Select values from dict starting with specified prefix.
#
# Parameters:
#   d - dict to select from
#   prefix - prefix to look for
#
# Return:
#   Dict with selected values
#
#********************************************************************************
def filterByPrefix(d, prefix):
  res = {}
  for k, v in d.iteritems():
    if k.find(prefix + '.') == 0:
      res[k[len(prefix) + 1:]] = v
  return res

#********************************************************************************
# Run 'make' command.
#
# Parameters:
#   path - path to directory in which make should be run
#   options - options to pass to make
#   clean - invoke 'clean' target
#
# Return:
#   True - make finished with no errors
#   False - some error occured
#
#********************************************************************************
def make(path, options, clean = True, parallel = False):
  if not build:
    return True
  result = True

  tempName = tempfile.mktemp()
  fd = open(tempName, 'w')
  for name, value in options.iteritems():
    fd.write('override %s=%s\n' % (name, value))
  fd.close()

  if parallel:
    if clean:
      cmd = 'make fresh -C %s MAKEFILES=%s' % (path, tempName)
    else:
      threads = int(os.environ['NUMBER_OF_PROCESSORS']) + 1
      cmd = 'make -j%d all -C %s MAKEFILES=%s' % (threads, path, tempName)
  else:
    clean = {True: 'clean', False: ''}[clean]
    cmd = 'make %s all -C %s MAKEFILES=%s' % (clean, path, tempName)

  if os.system(cmd) != 0:
    log.error('Build failed at %s' % path)
    result = False

  removeFile(tempName)
  return result

#********************************************************************************
# Execute any command in a separate shell
#
# Parameters:
#   command - command to be executed
#   enableOutput - if true output of execution process will be printed on console
#
# Return:
#   return code and full output of a command
#
#********************************************************************************
def execute(command, enableOutput = True):
  p = Popen(command, shell = True, stdin = PIPE, stdout = PIPE, stderr = STDOUT, env = None)
  output = ''

  read = '1'
  while len(read) > 0:
    read = p.stdout.read(5)
    output += read
    if enableOutput:
      sys.stdout.write(read)

  p.wait()
  return p.returncode, output

#********************************************************************************
# Run configurator
#
# Parameters:
#   config - configuration XML file
#   path - path where to put resulting configuration file
#   options - options to be used for configuration
#
# Return:
#   True - finished with no errors
#   False - error occured
#
#********************************************************************************
def configurator(config, path, options = {}):
  params = []
  if 'BOARD' in options:
    params += ['BOARD']

  if 'RFCHIP' in options:
    params += ['RFCHIP']

  for par in options:
    if par not in params:
      params += [par]

  options = ' '.join(['%s=%s' % (str(p), str(options[p])) for p in params])
  ret, output = execute('configurator "%s" "%s/configuration.h" -a %s' %
    (config, path, options))
  if ret != 0:
    log.error('Build failed at %s: configurator returned %d' % (path, ret))
    print output
    return False
  return True

#********************************************************************************
# New style make
#
# Parameters:
#   path - path to directory in which make should be run
#   stack - stack settings should be used to guess poject/config names
#           and passed to make
#   app - application settings should be used to guess poject/config names
#         and passed to make
#
# Return:
#   True - make finished with no errors
#   False - some error occured
#
#********************************************************************************
def make_(path, stack, app, parallel = False):
  if not build:
    return True

  project, config = guess.projectAndConfigName(cdicts(stack, app))
  fullPath = os.path.join(path, 'makefiles', project)

  if not configurator(os.path.join(path, runOn['config']), path, app):
    return False

  if parallel:
    threads = int(os.environ['NUMBER_OF_PROCESSORS']) + 1
    ret, output = execute('make fresh -j%d -C "%s" -f %s' % (threads, fullPath, 'Makefile_' + config))
  else:
    ret, output = execute('make clean all -C "%s" -f %s' % (fullPath, 'Makefile_' + config))

  if ret != 0:
    log.error('make clean all %s/%s at %s failed, return code = %d' %
      (project, config, path, ret))
    return False

  return True

#********************************************************************************
# Remove file.
#
# Parameters:
#   name - file name to remove
#
# Return:
#   none
#
#********************************************************************************
def removeFile(name):
  if os.path.exists(name):
    try:
      os.remove(name)
    except:
      log.error('Failed to remove temporary file %s' % name)

#********************************************************************************
# Create directory and all required directories on the path to it.
#
# Parameters:
#   path - path to directory
#
# Return:
#   True - no errors
#   False - error occured
#
#********************************************************************************
def makeDirs(path):
  if os.path.exists(path):
    return True

  try:
    os.makedirs(path)
  except:
    log.error('makeDirs: failed to create directory %s' % path)
  return True

#********************************************************************************
# Update test case statistics
#
# Parameters:
#   case - test case name
#   result - result of execution (True - pass, False - fail)
#
# Return:
#   none
#
#********************************************************************************
def updateTestCaseStatistics(case, result):
  logPath = env.getValue('logPath')
  if logPath is None:
    logPath = '.'
  statFileName = os.path.join(logPath, statisticsFileName)

  if not os.path.isfile(statFileName):
    return

  stat = {}
  lines = open(statFileName, 'r').readlines()
  for line in lines:
    if len(line):
      s = line.split()
      if len(s) != 3:
        log.write('Invalid statistics file format. Statistics was not updated for %s.' % s, log = 'suite')
        return
      else:
        stat[s[0]] = {True: int(s[1]), False: int(s[2])}

  if case not in stat:
    stat[case] = {True: 0, False: 0}

  stat[case][result] += 1

  lines = ['%s %d %d' % (st, stat[st][True], stat[st][False]) for st in stat]
  f = open(statFileName, 'w')
  try:
    for line in lines:
      f.write(line + '\n')
  finally:
    f.close()

#********************************************************************************
# Form certification test image name using test case variables.
#
# Parameters:
#   confName - configuration name
#
# Return:
#   Certification test image full name
#
#********************************************************************************
def getCertTestImageName(confName):
  certImagesPath = env.getValue('certImagesPath')
  if certImagesPath == None:
    #log.error('Path to certification test images is not specified. Use default.', log = 'suite')
    scriptsPath = env.getValue('scripts')
    certImagesPath = scriptsPath + '/certification/stack/ZigBee/configs/' + confName
  return certImagesPath + '/' + guess.certPrecompiledImageName(confName)
  
#********************************************************************************
# Build set of images with specified parameters in efficient way. Put images to
# cache for later use.
#
# Parameters:
#   reqired - list of required image parameters in natural format
#   prefix - path prefix
#   name - expected resulting file name
#   style - build style (old/new), temporary
#
# Return:
#   Number of images built (or already available in the cache)
#
#********************************************************************************
def buildRequiredImages(required, prefix, name, style):
  return 1

  stackPath = env.getValue('stackPath')
  halPath = env.getValue('halPath')
  appPath = os.path.join(env.getValue('appPath'), prefix)

  nodesNeeded = 0
  cStack, cHal = None, None
  for stack, hal, app in required:
    if '__spConfName' in stack:
      fullName = getCertTestImageName(stack['__spConfName'])
      name = fullName
      
    if cache.getRecord(name, (stack, hal, app)):
      nodesNeeded += 1
      continue # image already in cache

    if '__spConfName' not in stack:
      if 'SECURITY_MODE' not in stack.keys():
        if cStack is not None and 'SECURITY_MODE' in cStack.keys():
          newParam = {'SECURITY_MODE': cStack['SECURITY_MODE']}
          stack = cdicts(stack, newParam)
          app = cdicts(app, newParam)

      if stack != cStack:
        if make(stackPath, stack, parallel = True):
          cStack, cHal = stack, None
        else:
          cStack = None
          log.error('Stack build failed. Parameters:', log = 'suite')
          log.printOptions(stack)
          continue

      if hal != cHal:
        if make(halPath, hal):
          cHal = hal
        else:
          cHal = None
          log.error('HAL build failed. Parameters:', log = 'suite')
          log.printOptions(stack)
          log.printOptions(hal)
          continue

      if style == 'old':
        fullName = os.path.join(appPath, name)
        if not make(appPath, app):
          log.error('Application build failed. Parameters:', log = 'suite')
          log.printOptions(stack)
          log.printOptions(hal)
          log.printOptions(app)
          continue
      else: #new
        project, config = guess.projectAndConfigName(cdicts(stack, app))
        fullName = os.path.join(appPath, 'makefiles', project, config, 'Exe', name)
        if not make_(appPath, stack, app, parallel = True):
          log.error('Application build failed. Parameters:', log = 'suite')
          log.printOptions(stack)
          log.printOptions(hal)
          log.printOptions(app)
          continue

    cache.putRecord(fullName, name, (stack, hal, app))
    nodesNeeded += 1
  return nodesNeeded

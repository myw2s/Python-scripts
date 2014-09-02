import os
import sys
import time
import traceback
from com.atmel.wsnrunner import LogFactory
from com.atmel.wsnrunner import TesterException
import env
import exc
import log
import misc
import cache
import nodes
import public
import scriptInfo
from public import *

#********************************************************************************
# Process list of cases. For every case next actions are performed:
#  * Description is read and parsed
#  * List of variables to pass while execution is generated
#  * Check if all passed variables are expected inside list
#  * Final list of build parameters is generated
#  * Build parameters are updated with information from __buildType variable
#    ('COMMON' or 'SEPARATE')
#
# Parameters:
#   caseList - list of cases to process
#   nodesAvail - amount of nodes available to test system
#
# Return:
#   Processed list of cases.
#
#********************************************************************************
def expandCaseList(caseList, nodesAvail):
  commonDeviceParameters = {
    'coordinator': 'ALL_DEVICES_TYPES',
    'router'     : 'ALL_DEVICES_TYPES',
    'enddevice'  : 'ALL_DEVICES_TYPES',
    'all'        : 'ALL_DEVICES_TYPES'
  }
  separateDeviceParameters = {
    'coordinator': 'COORDINATOR',
    'router'     : 'ROUTER',
    'enddevice'  : 'ENDDEVICE',
    'all'        : 'ALL_DEVICES_TYPES'
  }

  envOpts = env.getOptions()
  extList = []
  for caseName, caseParameters in caseList.iteritems():
    fullName = misc.expandPath(caseName)
    if fullName is None:
      log.error('%s: file not found' % caseName, log = 'suite')
      continue

    try:
      info = scriptInfo.getScriptInfo(fullName)
    except scriptInfo.GetScriptInfoError, exception:
      log.error('%s: %s' % (caseName, str(exception)), log = 'suite')
      continue

    if info['type'] != 'testcase':
      log.error('%s: only testcases are allowed to be in test suite' % caseName, log = 'suite')
      continue

    if len(info['conns']) > nodesAvail:
      log.error('%s: not enough nodes to run this case' % caseName, log = 'suite')
      continue

    for buildParameters, variables in caseParameters:
      variables = misc.evalValues(misc.cdicts(env.getVariables(), info['variables'], variables))

      if misc.checkExpectedVariables:
        for var in variables:
          if var not in info['variables']:
            log.write('%s: variable "%s" is not expected inside script' % (caseName, var), log = 'suite')

      if '__buildType' in variables and variables['__buildType'] == 'SEPARATE':
        deviceParametersList = separateDeviceParameters
      else:
        deviceParametersList = commonDeviceParameters

      connParameters = {}
      for conn, connOptions in info['conns'].iteritems():
        if '__spConfName' not in variables:
          cType, cPort, cConf = connOptions

          deviceParameters = {
            'app.STACK_TYPE'  : deviceParametersList[cType],
            'stack.STACK_TYPE': deviceParametersList[cType]
          }

          cParameters = misc.cdicts(envOpts, info['configuration'],
            buildParameters, cConf, deviceParameters)
          connParameters[conn] = public.separateOptions(cParameters)
        else:
          stack = {'__spConfName': variables['__spConfName']}
          connParameters[conn] = (stack, {}, {})

      extList += [(caseName, connParameters, variables)]

  return extList

#********************************************************************************
# Build images required for testsuite
#
# Parameters:
#   caseList - list of cases in testsuite
#
# Return:
#   Number of images built (or already available in the cache)
#
#********************************************************************************
def buildImagesForTestSuite(caseList):
  required = []
  for caseName, connParameters, variables in caseList:
    for conn, parameters in connParameters.iteritems():
      if parameters not in required:
        required += [parameters]
  required.sort()
  r = misc.buildRequiredImages(required, misc.runOn['path'], misc.runOn['srec'],
      misc.runOn['style'])
  return r

#********************************************************************************
# Split case list into minimum amount of groups of maximum size (but not
# larger than nodesAvail)
#
# Parameters:
#   caseList - list of cases in testsuite
#   nodesAvail - amount of nodes available for test
#
# Return:
#   List of groups each containing indexes of cases from caseList.
#
#********************************************************************************
def groupCases(caseList, nodesAvail):
  # Extract lists of parameters required by cases
  requires = []

  for i in range(len(caseList)):
    caseName, connParameters, variables = caseList[i]

    featureParams = []
    for conn, parameters in connParameters.iteritems():
      if parameters not in featureParams:
        featureParams.append(parameters)
    caseParams = [parameters for conn, parameters in connParameters.iteritems()]
    nodesRequired = len(caseParams)
    
    placed = False
    for conf in requires:
      if featureParams == conf['featureParams']:
        for node in conf['nodes']:
          if node['parameters'] in caseParams:
            nodesRequired -= 1

        if (nodesRequired + len(conf['nodes'])) <= nodesAvail:
          placed = True
          for conn, parameters in connParameters.iteritems():
            connPlaced = False
            for node in conf['nodes']:
              if parameters == node['parameters'] and caseName not in node['cases']:
                node['cases'][caseName] = [i, conn]
                connPlaced = True
                break

            if not connPlaced:
              node = {
                 'parameters' : parameters, 
                 'cases' : {
                      caseName : [i, conn]
                 }
              }
              conf['nodes'].append(node)

    if not placed:
      conf = {'featureParams' : featureParams, 'nodes' : []}
      for conn, parameters in connParameters.iteritems():
        node = {'parameters' : parameters, 'cases' : {caseName : [i, conn]}}
        conf['nodes'].append(node)
      requires.append(conf)

  # Group cases
  groups = []
  groupUsedNodesCounters = []
  for conf in requires:
    placed = False
    
    for j in range(len(groups)):
      nodesInUse = groupUsedNodesCounters[j]
      if (len(conf['nodes']) + nodesInUse) <= nodesAvail:
        for node in conf['nodes']:
          groupUsedNodesCounters[j] += 1
          for testcase in node['cases']:
            index, conn = node['cases'][testcase]
            if index not in groups[j]:
              groups[j].append(index)
        placed = True
        break

    if not placed:
      newGroup = []
      nodesInUse = 0
      for node in conf['nodes']:
        nodesInUse += 1
        for testcase in node['cases']:
          index, conn = node['cases'][testcase]
          if index not in newGroup:
            newGroup.append(index)
      groupUsedNodesCounters.append(nodesInUse)
      groups.append(newGroup)

  return groups

#********************************************************************************
# Upload nodes required to run group of cases
#
# Parameters:
#   nodesList - list of available nodes
#   caseList - list of cases in testsuite
#   group - list of indexes of cases from caseList
#
# Return:
#   List of nodes used for this group.
#
#********************************************************************************
def uploadNodesFromGroup(nodesList, caseList, group):
  # Generate upload list
  reqs = []
  for index in group:
    caseName, connParameters, variables = caseList[index]
    req = []
    for conn, parameters in connParameters.iteritems():
      if '__spConfName' not in variables:
        tag = misc.runOn['srec']
      else:
        tag = misc.getCertTestImageName(variables['__spConfName'])
      req += [(tag, parameters)]
    
    reqs += [req]

  uploadList = misc.clists(reqs)

  nodeNames = [node.getName() for node in nodesList]
  nodes.setStatus(nodeNames, '%s: uploading' % misc.testSuiteName)

  # Upload nodes
  usedNodes = []
  
  # WLA: Disable upload feature
  misc.upload = False
  
  if misc.upload:
    for i in range(len(uploadList)):
      tag, parameters = uploadList[i]
      name = cache.getRecord(tag, parameters)
      nodesList[i].uploadFirmware(name)
    for i in range(len(uploadList)):
      if nodesList[i].waitNode():
        tag, parameters = uploadList[i]
        usedNodes += [(parameters, nodesList[i])]
      else:
        log.error('Upload to node %s failed' % nodesList[i].getName(), log = 'suite')
  else:
    for i in range(len(uploadList)):
      tag, parameters = uploadList[i]
      usedNodes += [(parameters, nodesList[i])]

  nodes.setStatus(nodeNames, misc.testSuiteName)

  return usedNodes

#********************************************************************************
# Run single case from group.
#
# Parameters:
#   case - test case name
#   nodesList - list of nodes
#   logPath - path to log directory
#   logName - base for log file name
#
# Return:
#   none
#
#********************************************************************************
def runCaseFromGroup(case, nodesList, logPath):
  caseName, connParameters, variables = case
  variables = misc.cdicts(env.getVariables(), variables)
  logName = '%s.txt' % caseName

  nodeNames = [node.getName() for nPar, node in nodesList]
  nodes.setStatus(nodeNames, '%s: running %s' % (misc.testSuiteName, caseName))

  nodeList = []
  taken = [False] * len(nodesList)
  for conn, cPar in connParameters.iteritems():
    for i in range(len(nodesList)):
      nPar, node = nodesList[i]
      if cPar == nPar and not taken[i]:
        taken[i] = True
        variables[conn] = node.getConnection()
        nodeList += [node]
        time.sleep(0.5)
        variables[conn].clear()
        break

  if len(nodeList) != len(connParameters):
    log.error('%s: not executed due to upload failure' % caseName, log = 'suite')
    return False

  nodes.restart(nodeList)
  #time.sleep(5)

  #LogFactory.dropPrefix('system')
  caseLogName = os.path.join(logPath, logName)
  log.open(caseLogName, enableConsole = False)

  # Write case parameters to log
  try:
    info = scriptInfo.getScriptInfo(misc.expandPath(caseName))
    descr = info['description'][0]
  except scriptInfo.GetScriptInfoError, exception:
    descr = '*** no description available ***'

  log.write('Case       : %s' % (caseName, ), log = 'suite')
  log.write('Description: %s' % (descr, ), log = 'suite')
  log.write('Connections:', log = 'suite')
  for conn, cPar in connParameters.iteritems():
    log.write('  %s (%s):' % (conn, variables[conn].getName()), log = 'suite')
    log.printCompressedOptions(cPar, log = 'suite')
  log.write('Variables  :', log = 'suite')
  for k, v in variables.iteritems():
    log.write('  %s = %s' % (k, v), log = 'suite')

  result = False
  try:
    vars = globals().copy()
    vars.update(variables)
    if '.py' != caseName[-len('.py'):]:
      vars['scriptPath'] = misc.expandPath(caseName)[:-len(caseName + '.py')]
    else:
      vars['scriptPath'] = misc.expandPath(caseName)[:-len(caseName)]
    execfile(misc.expandPath(caseName), vars, vars)
    log.write('%s: success' % caseName, log = 'suite')
    LogFactory.closeLogger('system')  # close log so file could be removed
    misc.removeFile(caseLogName)
    result = True
  except exc.TestFailed, exception:
    if exception.getMessage() is None:
      tb = traceback.extract_tb(sys.exc_info()[2])
      log.error('%s: fail (%s)' % (caseName, misc.formatFailMsg(tb[-2])))
    else:
      log.error(str(exception))
    log.error('%s: fail (see full log in %s)' % (caseName, logName), log = 'suite')

  except TesterException:
    log.error('%s: test environment internal error' % caseName, log = 'suite')

  except:
    log.printTraceback()
    log.error('%s: fail (see full log in %s)' % (caseName, logName), log = 'suite')

  misc.updateTestCaseStatistics(caseName, result)

  nodes.setStatus(nodeNames, misc.testSuiteName)
  nodes.restart(nodeList, leaveOff = True)
  time.sleep(1)

  return result

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
  t0 = time.time()
  
  logPath = env.getValue('logPath')
  if logPath is None:
    logPath = '.'

  logName = env.getValue('logName')
  if logName:
    logName = os.path.join(logPath, logName)
  else:
    logName = os.path.join(logPath, '%s_%s' % (misc.testSuiteName, misc.getTimeStr()))

  if not misc.makeDirs(logName):
    return

  misc.removeFile(logName + '.txt')
  log.open(logName + '.txt', log = 'suite', enableConsole = False)

  nodeList = env.getNodeList(10000, respectLimit = True) # Get as many as we can
  nodesAvail = len(nodeList)

  nodes.setStatus(nodeList, '%s: preparing' % misc.testSuiteName)

  result = {True: 0, False: 0}

  # Extract all required info from cases and build all images
  extList = expandCaseList(caseList, nodesAvail)
  cache.init()
  
  t1 = time.time()
#  buildImagesForTestSuite(extList)
  buildTime = time.time() - t1
  cache.sync()

  # Remove cases without all required images built
  workList = []
  fullSet = []
  for caseName, connParameters, variables in extList:
    workList += [(caseName, connParameters, variables)]
    fullSet = misc.clists([fullSet, [par for conn, par in connParameters.iteritems()]])

  nodesNeeded = len(fullSet)

  if nodesAvail < nodesNeeded:
    log.write('Info: for maximum performance %d nodes required (%d nodes available)' %
      (nodesNeeded, nodesAvail), log = 'suite')
  else:
    log.write('Info: %d nodes will be used' % nodesNeeded, log = 'suite')
    nodesAvail = nodesNeeded
  
  # Group all scripts to optimize upload strategy
  groups = groupCases(workList, nodesAvail)
  log.write('Info: %d uploads will be performed' % len(groups), log = 'suite')
  
  
  # Upload and execute scripts
  nodeList = nodeList[:nodesAvail]
  allNodes = []
  log.write('Test will use next nodes:', log = 'suite')
  for node in nodeList:
    log.write('  %s' % node, log = 'suite')
    allNodes += [misc.__nodeFactory.create(node)]

  #for node in allNodes:
  #  node.getConnection().setTesterMode(misc.runOn['tester'])

  testCaseExecTimes = []
  uploadTimes = []
  nodes.restart(allNodes, leaveOff = True)
  groupNo = 1

  for group in groups:
    log.write('Running group %d of %d' % (groupNo, len(groups)), log = 'suite')
    t2 = time.time()
    usedNodes = uploadNodesFromGroup(allNodes, workList, group)
    uploadTimes.append(time.time() - t2)
    time.sleep(1)
    for index in group:
      t3 = time.time()
      ret = runCaseFromGroup(workList[index], usedNodes, logName)
      testCaseExecTimes.append(time.time() - t3)
      result[ret] += 1
    groupNo += 1

  if len(uploadTimes):
    meanUploadTime = sum(uploadTimes) / len(uploadTimes)
  else:
    meanUploadTime = 0

  if len(testCaseExecTimes):
    meanTestcaseExecTime = sum(testCaseExecTimes) / len(testCaseExecTimes)
  else:
    meanTestcaseExecTime = 0

  totalTime = time.time() - t0
  
  log.write('Test finished: %d passed, %d failed' % (result[True], result[False]), log = 'suite')
  log.write('Execution time statistics', log = 'suite')
  log.write('Build images time: %d sec' % buildTime, log = 'suite')
  log.write('Total upload time: %d sec' % sum(uploadTimes), log = 'suite')
  log.write('Mean group upload time: %d sec' % meanUploadTime, log = 'suite')
  log.write('Testcases execution time: %d sec' % sum(testCaseExecTimes), log = 'suite')
  log.write('Mean testcase execution time: %d sec' % meanTestcaseExecTime, log = 'suite')
  log.write('Total execution time: %d sec' % totalTime, log = 'suite')

  # Remove all temporary files, save cache
  cache.cleanup()

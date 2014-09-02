import re
import misc

#********************************************************************************
# Exception used by getScriptInfo() to indicate error.
#********************************************************************************
class GetScriptInfoError(Exception):
  def __init__(self, msg):
    self.__msg = msg

  def __str__(self):
    return 'GetScriptInfoError: %s' % self.__msg

#********************************************************************************
# Parse list of standard expressions in form of 'param = value'.
#
# Parameters:
#   extInfo - list of expressions in form of 'param = value'
#
# Return:
#   Dict with parsed information.
#
#********************************************************************************
def parseConfigParameters(extInfo):
  reConfRecord = re.compile(' *(?P<param>[\.|\w]+) *= *(?P<value>.+)')
  res = {}
  for info in extInfo:
    if info.strip() == '':
      continue

    match = reConfRecord.match(info)
    if match:
      res[match.group('param').strip()] = match.group('value').strip()
    else:
      raise GetScriptInfoError('Invalid configuration record format: %s' % info)

  return res

#********************************************************************************
# Read and parse standard script header.
#
# Parameters:
#   name - short name of script which description is required
#
# Return:
#   Description parsed and prepared for further processing.
#
#********************************************************************************
def getScriptInfo(name):
  # Extarct first comment section (description section) from file
  scriptInfo = None
  for line in open(name, 'r').readlines():
    if line.strip() in ['"""', "'''"]:
      if scriptInfo is not None:
        break
      else:
        scriptInfo = []
    else:
      if scriptInfo is not None:
        scriptInfo += [line]

  if scriptInfo is None:
    raise GetScriptInfoError('Script description not found')

  # Split extracted section into separate tags
  scriptTypes = ['sampleapptest', 'sampleapp', 'testcase', 'testsuite', 'function', 'rawfile']
  validTags = scriptTypes + ['description', 'tags', 'configuration', 'connection', 'variables', 'runon','parameters','returns']

  reTag = re.compile('@(?P<name>\w+) *(?P<short>.*)')
  tags = []
  cTag = None
  for line in scriptInfo:
    match = reTag.match(line)
    if match:
      if cTag:
        tags += [(cTag, cShort, cExt)]

      cTag = match.group('name')
      if cTag not in validTags:
        raise GetScriptInfoError('Invalid tag name: %s' % cTag)
      cShort = match.group('short')
      cExt = []
    else:
      if cTag:
        cExt += [line]
      else:
        raise GetScriptInfoError('Extended info outside the tag detected')

  # append last tag info
  if cTag:
    tags += [(cTag, cShort, cExt)]

  # handle short and ext data depending on tag type
  reConnection = re.compile(' *(?P<conn>[\w|\d]+) *= *(?P<type>\w+)( *, *(?P<port>\S+))?')

  res = {}
  conns = {}
  res['conns'] = conns
  res['variables'] = {}
  res['configuration'] = {}
  res['runon'] = 'stack'
  for cTag, cShort, cExt in tags:
    if cTag in scriptTypes:
      res['type'] = cTag

    elif cTag == 'description':
      res['description'] = [cShort, ''.join(cExt)]

    elif cTag == 'tags':
      res['tags'] = (cShort + ' '.join(cExt)).split()

    elif cTag == 'runon':

     if cShort in misc.runOnOptions:
        res['runon'] = cShort
     else:
        raise GetScriptInfoError('Invalid runner type: "%s"' % cShort)

    elif cTag == 'configuration':
      res['configuration'] = parseConfigParameters(cExt)

    elif cTag == 'variables':
      res['variables'] = parseConfigParameters(cExt)

    elif cTag == 'connection':
      match = reConnection.match(cShort)
      if match:
        conn = match.group('conn')
        type = match.group('type')
        port = match.group('port')
        conf = parseConfigParameters(cExt)
        if type in ['all', 'coordinator', 'router', 'enddevice']:
          conns[conn] = (type, port, conf)
        else:
          raise GetScriptInfoError('Incorrect device type: %s' % type)

      else:
        raise GetScriptInfoError('Invalid connection information: "%s"' % cShort)

  # some final checks
  for exp in ['type', 'description']:
    if exp not in res:
      raise GetScriptInfoError('"%s" field is missing in script info' % exp)

  return res

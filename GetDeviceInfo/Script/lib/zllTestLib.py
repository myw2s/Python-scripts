"""
@description ZLL test library. Required for TestHarness emulation. 
             This file should be placed in Atmel/WSNRunner/lib directory, to allow easy including
             in ZLL test cases.
"""

#*****************************************************************************************
# Defines section
#*****************************************************************************************
extPANId  = 0xDEADBEEFCAFEACAB
shortPANId = 0xACAB
tcExtAddr = 0xAAAAAAAAAAAAAAAA
tcShortAddr = 0x0000
lightShortAddr = 0x0002
lightExtAddr = 0x000425ffff174dc6
remoteExtAddr = 0x000425ffff174df3
remoteShortAddr = 0x0001
lightEndpoint = 0x0A
remoteEndpoint = 0x01
nwkKey = {"nwkKey": [0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xAA,0xBB,0xCC,0xDD,0xEE,0xFF,0x00]}
preconfiguredNetworkKey = {"ZDO Status": 0x00}
tcZllEndponint = 0x01

globalGroupId = 0x0001

#
# Commands list
#

# - General ZCL Frame Format
#         [FrameCtrl] [FrameSeqNum] [CommandId] [Payload]
# Bytes        1            1            1          n

# -- Frame Control Field
#         [Rsrvd] [DisableDefaultResp] [Direction] [ManufSpec] [FrameType]
# Bits      7-5            4                3           2          1-0
#
# --- FrameType: 1 - clusterSpecific; 0 - entire profile.
# --- Direction: 1 - server to client; 0 - client to server.
#

# Status values
SUCCESS                     = 0x00
UNSUP_CLUSTER_COMMAND       = 0x81
UNSUP_MANUF_CLUSTER_COMMAND = 0x83
UNSUP_MANUF_GENERAL_COMMAND = 0x84
INVALID_VALUE               = 0x87
NOT_FOUND                   = 0x8B

# Color values
RED_X    = 41942
RED_Y    = 20971
GREEN_X  = 19660
GREEN_Y  = 39321
BLUE_X   = 9830
BLUE_Y   = 3932
BLUE_HUE = 180
BLUE_ENHANCED_HUE = (BLUE_HUE << 8)

# Device IDs
colorLightDeviceId           = 0x0200
colorSceneControllerDeviceId = 0x0810

# Profile IDs
homeAutomationProfileId = 0x0104
lightLinkProfileId      = 0xC05E

# Attribute types
boolAttrType            = 0x10
bitmap8Type             = 0x18
bitmap16Type            = 0x19
uint8AttrType           = 0x20
uint16AttrType          = 0x21
enum8AttrType           = 0x30
characterStringAttrType = 0x42

# Cluster Ids
basicClusterId            = 0x0000
identifyClusterId         = 0x0003
groupsClusterId           = 0x0004
scenesClusterId           = 0x0005
onOffClusterId            = 0x0006
levelControlClusterId     = 0x0008
colorControlClusterId     = 0x0300
zllCommissioningClusterId = 0x1000

#
# Attributes
#

# Basic
zclVersionAttrId       =  0x0000
appVersionAttrId       =  0x0001
stackVersionAttrId     =  0x0002
hwVersionAttrId        =  0x0003
manufacturerNameAttrId =  0x0004
modelIdAttrId          =  0x0005
dateCodeAttrId         =  0x0006
powerSourceAttrId      =  0x0007
swBuildIdAttrId        =  0x4000

# Identify
identifyTimeAttrId = 0x0000

# Groups
nameSupportAttrId = 0x0000

# Scenes
sceneCountAttrId   = 0x0000
currentSceneAttrId = 0x0001
currentGroupAttrId = 0x0002
sceneValidAttrId   = 0x0003
nameSupportAttrId  = 0x0004

# On/Off
onOffAttrId              = 0x0000
globalSceneControlAttrId = 0x4000
onTimeAttrId             = 0x4001
onOffWaitTimeAttrId      = 0x4002

# Level Control
currentLevelAttrId    = 0x0000
lcRemainingTimeAttrId = 0x0001

# Color Control
currentHueAttrId                 = 0x0000
currentSaturationAttrId          = 0x0001
ccRemainingTimeAttrId            = 0x0002
currentXAttrId                   = 0x0003
currentYAttrId                   = 0x0004
colorModeAttrId                  = 0x0008
numberOfPrimariesAttrId          = 0x0010
primary1XAttrId                  = 0x0011
primary1YAttrId                  = 0x0012
primary1IntensityAttrId          = 0x0013
primary2XAttrId                  = 0x0015
primary2YAttrId                  = 0x0016
primary2IntensityAttrId          = 0x0017
primary3XAttrId                  = 0x0019
primary3YAttrId                  = 0x001A
primary3IntensityAttrId          = 0x001B
primary4XAttrId                  = 0x0020
primary4YAttrId                  = 0x0021
primary4IntensityAttrId          = 0x0022
primary5XAttrId                  = 0x0024
primary5YAttrId                  = 0x0025
primary5IntensityAttrId          = 0x0026
primary6XAttrId                  = 0x0028
primary6YAttrId                  = 0x0029
primary6IntensityAttrId          = 0x002A
enhancedCurrentHueAttrId         = 0x4000
enhancedColorModeAttrId          = 0x4001
colorLoopActiveAttrId            = 0x4002
colorLoopDirectionAttrId         = 0x4003
colorLoopTimeAttrId              = 0x4004
colorLoopStartEnhancedHueAttrId  = 0x4005
colorLoopStoredEnhancedHueAttrId = 0x4006
colorCapabilitiesAttrId          = 0x400A

#
# Commands
#

# General
readAttrReqCmd           = [0x10, 0x2A, 0x00]
readAttrRespCmd          = [0x18, 0x2A, 0x01]
writeAttrReqCmd          = [0x10, 0x2A, 0x02]
writeAttrUndividedReqCmd = [0x10, 0x2A, 0x03]
writeAttrRespCmd         = [0x18, 0x2A, 0x04]
writeAttrNoRespCmd       = [0x10, 0x2A, 0x05]
defaultRespCmd           = [0x18, 0x2A, 0x0B]

specWriteAttrReqCmd = [0x14, 0x00, 0x00, 0x2A, 0x02]
specDefaultRespCmd  = [0x1C, 0x00, 0x00, 0x2A, 0x0B]

# Identify
identifyCmd          = [0x11, 0x2A, 0x00]
identifyQueryCmd     = [0x11, 0x2A, 0x01]
identifyQueryRespCmd = [0x19, 0x2A, 0x00]
triggerEffectCmd     = [0x11, 0x2A, 0x40]

specIdentifyCmd = [0x15, 0x00, 0x00, 0x2A, 0x00]

# On/Off
offCmd                     = [0x11, 0x2A, 0x00]
onCmd                      = [0x11, 0x2A, 0x01]
toggleCmd                  = [0x11, 0x2A, 0x02]
offWithEffectCmd           = [0x11, 0x2A, 0x40]
onWithRecallGlobalSceneCmd = [0x11, 0x2A, 0x41]
onWithTimedOffCmd          = [0x11, 0x2A, 0x42]

# Groups
addGroupCmd               = [0x11, 0x2A, 0x00]
addGroupRespCmd           = [0x19, 0x2A, 0x00]
viewGroupCmd              = [0x11, 0x2A, 0x01]
viewGroupRespCmd          = [0x19, 0x2A, 0x01]
getGroupMembershipCmd     = [0x11, 0x2A, 0x02]
getGroupMembershipRespCmd = [0x19, 0x2A, 0x02]
removeGroupCmd            = [0x11, 0x2A, 0x03]
removeGroupRespCmd        = [0x19, 0x2A, 0x03]
removeAllGroupsCmd        = [0x11, 0x2A, 0x04]
addGroupIfIdentifyingCmd  = [0x11, 0x2A, 0x05]

# Scenes
addSceneCmd               = [0x11, 0x2A, 0x00]
addSceneRespCmd           = [0x19, 0x2A, 0x00]
viewSceneCmd              = [0x11, 0x2A, 0x01]
viewSceneRespCmd          = [0x19, 0x2A, 0x01]
removeSceneCmd            = [0x11, 0x2A, 0x02]
removeSceneRespCmd        = [0x19, 0x2A, 0x02]
removeAllScenesCmd        = [0x11, 0x2A, 0x03]
removeAllScenesRespCmd    = [0x19, 0x2A, 0x03]
storeSceneReqCmd          = [0x11, 0x2A, 0x04]
storeSceneRespCmd         = [0x19, 0x2A, 0x04]
recallSceneCmd            = [0x11, 0x2A, 0x05]
getSceneMembershipCmd     = [0x11, 0x2A, 0x06]
getSceneMembershipRespCmd = [0x19, 0x2A, 0x06]
enhancedAddSceneCmd       = [0x11, 0x2A, 0x40]
enhancedAddSceneRespCmd   = [0x19, 0x2A, 0x40]
enhancedViewSceneCmd      = [0x11, 0x2A, 0x41]
enhancedViewSceneRespCmd  = [0x19, 0x2A, 0x41]
copySceneCmd              = [0x11, 0x2A, 0x42]
copySceneRespCmd          = [0x19, 0x2A, 0x42]

# Level Control
moveToLevelCmd          = [0x11, 0x2A, 0x00]
moveCmd                 = [0x11, 0x2A, 0x01]
stepCmd                 = [0x11, 0x2A, 0x02]
stopCmd                 = [0x11, 0x2A, 0x03]
moveToLevelWithOnOffCmd = [0x11, 0x2A, 0x04]
moveWithOnOffCmd        = [0x11, 0x2A, 0x05]
stepWithOnOffCmd        = [0x11, 0x2A, 0x06]
alterStopCmd            = [0x11, 0x2A, 0x07]

# Color Control
moveToHueCmd                      = [0x11, 0x2A, 0x00]
moveHueCmd                        = [0x11, 0x2A, 0x01]
stepHueCmd                        = [0x11, 0x2A, 0x02]
moveToSaturationCmd               = [0x11, 0x2A, 0x03]
moveSaturationCmd                 = [0x11, 0x2A, 0x04]
stepSaturationCmd                 = [0x11, 0x2A, 0x05]
moveToHueAndSaturationCmd         = [0x11, 0x2A, 0x06]
moveToColorCmd                    = [0x11, 0x2A, 0x07]
moveColorCmd                      = [0x11, 0x2A, 0x08]
stepColorCmd                      = [0x11, 0x2A, 0x09]
enhancedMoveToHueCmd              = [0x11, 0x2A, 0x40]
enhancedMoveHueCmd                = [0x11, 0x2A, 0x41]
enhancedStepHueCmd                = [0x11, 0x2A, 0x42]
enhancedmoveToHueAndSaturationCmd = [0x11, 0x2A, 0x43]
colorLoopSetCmd                   = [0x11, 0x2A, 0x44]
stopMoveStepCmd                   = [0x11, 0x2A, 0x47]

# ZLL Commissioning
endpointInformationCmd     = [0x09, 0x2A, 0x40]
getGroupIdentifiersReqCmd  = [0x11, 0x2A, 0x41]
getGroupIdentifiersRespCmd = [0x19, 0x2A, 0x41]
getEndpointListReqCmd      = [0x11, 0x2A, 0x42]
getEndpointListRespCmd     = [0x19, 0x2A, 0x42]

#*****************************************************************************************
# Fuctions section
#*****************************************************************************************

# General
def formReadAttrReq(attrList):
  list = []
  for attrId in attrList:
    list += u16ToRaw(attrId)
  return readAttrReqCmd[:] + list

def formReadAttrResp(attrList, status):
  command = readAttrRespCmd[:]
  for (attrId, attrType, attrValue) in attrList:
    command += (
    u16ToRaw(attrId) + 
    [status] +
    [attrType] + 
    attrValue)
  return command

def formWriteAttrReq(attrList):
  command = writeAttrReqCmd[:]
  for (attrId, attrType, attrValue) in attrList:
    command += (
    attrId + 
    [attrType] + 
    attrValue)
  return command

def formWriteAttrUndividedReq(attrList):
  command = writeAttrUndividedReqCmd[:]
  for (attrId, attrType, attrValue) in attrList:
    command += (
    attrId + 
    [attrType] + 
    attrValue)
  return command

def formWriteAttrNoResp(attrList):
  command = writeAttrNoRespCmd[:]
  for (attrId, attrType, attrValue) in attrList:
    command += (
    attrId + 
    [attrType] + 
    attrValue)
  return command

def formWriteAttrResp(attrList, status):
  command = writeAttrRespCmd[:]
  if status:
    for (attrId, attrType, attrValue) in attrList:
      command += (
      [status] +
      attrId)
  else:
    command += [status]
  return command

def formDefaultResp(commandId, statusCode):
  return defaultRespCmd[:] + [commandId] + [statusCode]

def formSpecWriteAttrReq(attrList):
  command = specWriteAttrReqCmd[:]
  for (attrId, attrType, attrValue) in attrList:
    command += (
    attrId + 
    [attrType] + 
    attrValue)
  return command

def formSpecDefaultResp(commandId, statusCode):
  return specDefaultRespCmd[:] + [commandId] + [statusCode]

# Identify
def formIdentify(identifyTime):
  return identifyCmd[:] + u16ToRaw(identifyTime)

def formIdentifyQueryResp(timeout):
  return identifyQueryRespCmd[:] + u16ToRaw(timeout)

def formTriggerEffect(effectId, effectVariant):
  return triggerEffectCmd[:] + [effectId] + [effectVariant]

def formSpecIdentify(identifyTime):
  return specIdentifyCmd[:] + u16ToRaw(identifyTime)

# On/Off
def formOffWithEffect(effectId, effectVariant):
  return offWithEffectCmd[:] + [effectId] + [effectVariant]

def formOnWithTimedOffCmd(onOffControl, onTime, offWaitTime):
  return onWithTimedOffCmd[:] + [onOffControl] + u16ToRaw(onTime) + u16ToRaw(offWaitTime)

# Groups
def formAddGroupReq(groupId):
  return (addGroupCmd[:] + 
         u16ToRaw(groupId) +
         stringAttrPayload(""))

def formAddGroupResp(groupId, status):
  return (addGroupRespCmd[:] +
         [status] +
         u16ToRaw(groupId))

def formViewGroupCmd(groupId):
  return viewGroupCmd[:] + u16ToRaw(groupId)

def formViewGroupRespCmd(status, groupId, groupName):
  return viewGroupRespCmd[:] + [status] + u16ToRaw(groupId) + stringAttrPayload(groupName)

def formGetGroupMembership(groupList):
  list = []
  for group in groupList:
    list += u16ToRaw(group)
  return getGroupMembershipCmd[:] + [len(groupList)] + list

def formGetGroupMembershipResp(capacity, groupCount, groupList):
  list = []
  for group in groupList:
    list += u16ToRaw(group)
  return getGroupMembershipRespCmd[:] + [capacity] + [groupCount] + list

def formRemoveGroupCmd(groupId):
  return removeGroupCmd[:] + u16ToRaw(groupId)

def formRemoveGroupRespCmd(status, groupId):
  return removeGroupRespCmd[:] + [status] + u16ToRaw(groupId)

def formAddGroupIfIdentifyingCmd(groupId):
  return addGroupIfIdentifyingCmd[:] + u16ToRaw(groupId) + stringAttrPayload("")

# Scenes
def formAddSceneCmd(groupId, sceneId, transitionTime):
  return addSceneCmd[:] + u16ToRaw(groupId) + [sceneId] + u16ToRaw(transitionTime) + stringAttrPayload("")

def formAddSceneRespCmd(status, groupId, sceneId):
  return addSceneRespCmd[:] + [status] + u16ToRaw(groupId) + [sceneId]

def formViewSceneCmd(groupId, sceneId):
  return viewSceneCmd[:] + u16ToRaw(groupId) + [sceneId]

def formViewSceneRespCmd(status, groupId, sceneId, transitionTime):
  response = viewSceneRespCmd[:] + [status] + u16ToRaw(groupId) + [sceneId] + u16ToRaw(transitionTime)
  response += stringAttrPayload("")
  return response

def formRemoveSceneCmd(groupId, sceneId):
  return removeSceneCmd[:] + u16ToRaw(groupId) + [sceneId]

def formRemoveSceneRespCmd(status, groupId, sceneId):
  return removeSceneRespCmd[:] + [status] + u16ToRaw(groupId) + [sceneId]

def formRemoveAllScenesCmd(groupId):
   return removeAllScenesCmd[:] + u16ToRaw(groupId)

def formRemoveAllScenesRespCmd(status, groupId):
  return removeAllScenesRespCmd[:] + [status] + u16ToRaw(groupId)

def formStoreSceneReqCmd(groupId, sceneId):
  return storeSceneReqCmd[:] + u16ToRaw(groupId) + [sceneId]

def formStoreSceneRespCmd(status, groupId, sceneId):
  return storeSceneRespCmd[:] + [status] + u16ToRaw(groupId) + [sceneId]

def formRecallSceneCmd(groupId, sceneId):
  return recallSceneCmd[:] + u16ToRaw(groupId) + [sceneId]

def formGetSceneMembershipCmd(groupId):
  return getSceneMembershipCmd[:] + u16ToRaw(groupId)

def formGetSceneMembershipRespCmd(status, capacity, groupId, sceneCount, sceneList):
  response = getSceneMembershipRespCmd[:] + [status] + [capacity] + u16ToRaw(groupId)
  if SUCCESS == status:
    response += [sceneCount] + sceneList
  return response

def formEnhancedAddSceneCmd(groupId, sceneId, transitionTime, onOffExt, levelControlExt, colorControlExt):
  request = enhancedAddSceneCmd[:] + u16ToRaw(groupId) + [sceneId] + u16ToRaw(transitionTime) + stringAttrPayload("")
  for (profileId, size, ext) in [onOffExt, levelControlExt, colorControlExt]:
    request += u16ToRaw(profileId) + [size] + ext
  return request

def formEnhancedAddSceneRespCmd(status, groupId, sceneId):
  return enhancedAddSceneRespCmd[:] + [status] + u16ToRaw(groupId) + [sceneId]

def formEnhancedViewSceneCmd(groupId, sceneId):
  return enhancedViewSceneCmd[:] + u16ToRaw(groupId) + [sceneId]

def formEnhancedViewSceneRespCmd(status, groupId, sceneId, transitionTime, onOffExt, levelControlExt, colorControlExt):
  response = enhancedViewSceneRespCmd[:] + [status] + u16ToRaw(groupId) + [sceneId]
  if SUCCESS == status:
    response += u16ToRaw(transitionTime) + stringAttrPayload("")
    for (clusterId, size, ext) in [onOffExt, levelControlExt, colorControlExt]:
      response += u16ToRaw(clusterId) + [size] + ext
  return response

def formCopySceneCmd(mode, groupIdFrom, sceneIdFrom, groupIdTo, sceneIdTo):
  return copySceneCmd[:] + [mode] + u16ToRaw(groupIdFrom) + [sceneIdFrom] + u16ToRaw(groupIdTo) + [sceneIdTo]

def formCopySceneRespCmd(status, groupIdFrom, sceneIdFrom):
  return copySceneRespCmd[:] + [status] + u16ToRaw(groupIdFrom) + [sceneIdFrom]

# Level Control
def formMoveToLevelCmd(level, transitionTime):
  return moveToLevelCmd[:] + [level] + u16ToRaw(transitionTime)

def formMoveCmd(moveMode, rate):
  return moveCmd[:] + [moveMode] + [rate]

def formStepCmd(stepMode, stepSize, transitionTime):
  return stepCmd[:] + [stepMode] + [stepSize] + u16ToRaw(transitionTime)

def formMoveToLevelWithOnOffCmd(level, transitionTime):
  return moveToLevelWithOnOffCmd[:] + [level] + u16ToRaw(transitionTime)

def formMoveWithOnOffCmd(moveMode, rate):
  return moveWithOnOffCmd[:] + [moveMode] + [rate]

def formStepWithOnOffCmd(stepMode, stepSize, transitionTime):
  return stepWithOnOffCmd[:] + [stepMode] + [stepSize] + u16ToRaw(transitionTime)

# Color Control
def formMoveToHueCmd(hue, direction, transitionTime):
  return moveToHueCmd[:] + [hue] + [direction] + u16ToRaw(transitionTime)

def formMoveHueCmd(moveMode, rate):
  return moveHueCmd[:] + [moveMode] + [rate]

def formStepHueCmd(stepMode, stepSize, transitionTime):
  return stepHueCmd[:] + [stepMode] + [stepSize] + u16ToRaw(transitionTime)

def formMoveToSaturationCmd(saturation, transitionTime):
  return moveToSaturationCmd[:] + [saturation] + u16ToRaw(transitionTime)

def formMoveSaturationCmd(moveMode, rate):
  return moveSaturationCmd[:] + [moveMode] + [rate]

def formStepSaturationCmd(stepMode, stepSize, transitionTime):
  return stepSaturationCmd[:] + [stepMode] + [stepSize] + u16ToRaw(transitionTime)

def formMoveToHueAndSaturationCmd(hue, saturation, transitionTime):
  return moveToHueAndSaturationCmd[:] + [hue] + [saturation] + u16ToRaw(transitionTime)

def formMoveToColorCmd(x, y, transitionTime):
  return moveToColorCmd[:] + u16ToRaw(x) + u16ToRaw(y) + u16ToRaw(transitionTime)

def formMoveColorCmd(rateX, rateY):
  return moveColorCmd[:] + u16ToRaw(rateX) + u16ToRaw(rateY)

def formStepColorCmd(stepX, stepY, transitionTime):
  return stepColorCmd[:] + u16ToRaw(stepX) + u16ToRaw(stepY) + u16ToRaw(transitionTime)

def formEnhancedMoveToHueCmd(enhancedHue, direction, transitionTime):
  return enhancedMoveToHueCmd[:] + u16ToRaw(enhancedHue) + [direction] + u16ToRaw(transitionTime)

def formEnhancedMoveHueCmd(moveMode, rate):
  return enhancedMoveHueCmd[:] + [moveMode] + u16ToRaw(rate)

def formEnhancedStepHueCmd(stepMode, stepSize, transitionTime):
  return enhancedStepHueCmd[:] + [stepMode] + u16ToRaw(stepSize) + u16ToRaw(transitionTime)

def formEnhancedmoveToHueAndSaturationCmd(hue, saturation, transitionTime):
  return enhancedmoveToHueAndSaturationCmd[:] + u16ToRaw(hue) + [saturation] + u16ToRaw(transitionTime)

def formColorLoopSetCmd(updateFlags, action, direction, time, startHue):
  return colorLoopSetCmd[:] + [updateFlags] + [action] + [direction] + u16ToRaw(time) + u16ToRaw(startHue)

# ZLL Commissioning
def formEndpointInformationCmd(ieeeAddr, nwkAddr, endpointId, profileId, deviceId, version):
  return endpointInformationCmd[:] + u64ToRaw(ieeeAddr) + u16ToRaw(nwkAddr) + [endpointId] + u16ToRaw(profileId) + u16ToRaw(deviceId) + [version]

def formGetGroupIdentifiersReqCmd(startIndex):
  return getGroupIdentifiersReqCmd[:] + [startIndex]

def formGetGroupIdentifiersRespCmd(total, startIndex, groupRecordList):
  cmd = getGroupIdentifiersRespCmd[:] + [total] + [startIndex] + [len(groupRecordList)]
  for (groupId, groupType) in groupRecordList:
    cmd += u16ToRaw(groupId) + [groupType]
  return cmd

def formGetEndpointListReqCmd(startIndex):
  return getEndpointListReqCmd[:] + [startIndex]

def formGetEndpointListRespCmd(total, startIndex, endpointRecordList):
  cmd = getEndpointListRespCmd[:] + [total] + [startIndex] + [len(endpointRecordList)]
  for (nwkAddr, endpointId, profileId, deviceId, version) in endpointRecordList:
    cmd += u16ToRaw(nwkAddr) + [endpointId] + u16ToRaw(profileId) + u16ToRaw(deviceId) + [version]
  return cmd

# Miscellaneous
def stringAttrPayload(string):
  payload = [ord(x) for x in string]
  return [len(payload)] + payload

def u16ToRaw(u16):
  msb = u16 >> 8
  lsb = u16 & 0xFF
  return [lsb, msb]

def u32ToRaw(u32):
  ms16 = u32 >> 16
  ls16 = u32 & 0xFFFF
  return u16ToRaw(ls16) + u16ToRaw(ms16)

def u64ToRaw(u64):
  ms32 = u64 >> 32
  ls32 = u64 & 0xFFFFFFFF
  return u32ToRaw(ls32) + u32ToRaw(ms32)

def looseCheck(x, y):
  looseX = [x[0]] + x[2:]
  looseY = [y[0]] + y[2:]
  return (looseX == looseY)


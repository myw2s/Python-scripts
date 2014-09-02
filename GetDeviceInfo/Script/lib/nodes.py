import time
import env
import log
import misc
import cache

#********************************************************************************
# Reset list of nodes.
#
# Parameters:
#   nodes - list of nodes to reset
#   leaveOff - leave nodes in Off state after reset
#
# Return:
#   none
#
#********************************************************************************
def restart(nodes, leaveOff=False):
  #for node in nodes:
  #  node.powerOff()
  time.sleep(1)
  for node in nodes:
    node.getConnection().clear()
    #if not leaveOff:
    #  node.powerOn()

#********************************************************************************
# Upload images to nodes. This function is fublic and must be used inside
# sample application tests.
# Be informed that test-suite runner uses it's own implementation of this function.
#
# Parameters:
#   nodes - list of nodes to use
#   tag - tag for identifying record in cache
#   images - list of separated image parameters of images to be uploaded
#
# Return:
#   True - all images uploaded successfully
#   False - some uploads are failed
#
#********************************************************************************
def uploadImages(nodes, tag, images):
  if not misc.upload:
    return True

  for i in range(len(nodes)):
    nodes[i].uploadFirmware(cache.getRecord(tag, images[i]))

  res = True
  for node in nodes:
    if not node.waitNode():
      log.error('Upload to node %s failed' % node.getName(), log = 'suite')
      res = False

  print '' # New line after upload progress indicator (dots)
  return res

#********************************************************************************
# Set UART parameters on network nodes.
#
# par is a dict and can have next parameters:
#  * speed   : 300, 600, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200 or 230400
#  * stopBits: 1 or 2
#  * parity  : 'None', 'Even' or 'Odd'
#  * bits    : 7 or 8
#  * flowCtrl: 'None', 'Xon/Xoff', 'Hardware' or 'Pass'
#
# Parameters:
#   nodes - list of nodes
#   par - parameters to set
#
# Return:
#   none
#
#********************************************************************************
def setParameters(nodes, par):
  for node in nodes:
    node.configureNode(par)
  for node in nodes:
    node.waitNode()

#********************************************************************************
# Send satatus of nodes to resource manager.
#
# Parameters:
#   nodes - list of nodes
#   status - status to send
#
# Return:
#   none
#
#********************************************************************************
def setStatus(nodes, status):
  for node in nodes:
    if misc.__client:
      misc.__client.setNodeStatus(node, status)

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
  localNodeList = env.getValue('nodes')

  if localNodeList and addr in localNodeList:
    return True

  if misc.__client:
    return misc.__client.getNode(addr)

  return False

import os
import re
import env
import log
import shutil
import random
import tempfile
import misc

__cacheRecords = None

#********************************************************************************
# Initialize cache.
#
# Parameters:
#   none
#
# Return:
#   none
#
#********************************************************************************
def init():
  global __cacheRecords
  __cacheRecords = []
  imageCachePath = env.getValue('imageCachePath')
  if imageCachePath is None:
    return

  try:
    fd = open(os.path.join(imageCachePath, 'cache'), 'r')
    cacheLines = fd.readlines()
    fd.close()
  except IOError:
    return

  info = []
  reCacheRecord = re.compile('(?P<tag>.+)#(?P<name>.+)#(?P<stack>.+)#(?P<hal>.+)#(?P<app>.+)#')
  for record in cacheLines:
    match = reCacheRecord.match(record)
    if match:
      tag = match.group('tag')
      name = match.group('name')
      stack = eval(match.group('stack'))
      hal = eval(match.group('hal'))
      app = eval(match.group('app'))
      info += [(tag, name, stack, hal, app)]
    else:
      return # Something wrong with cache
  __cacheRecords = info

#********************************************************************************
# Write cache records to disk.
#
# Parameters:
#   none
#
# Return:
#   none
#
#********************************************************************************
def writeRecords():
  global __cacheRecords
  imageCachePath = env.getValue('imageCachePath')
  if imageCachePath is None:
    return

  try:
    fd = open(os.path.join(imageCachePath, 'cache'), 'w')
    for rTag, rName, rStack, rHal, rApp in __cacheRecords:
      fd.write('%s#%s#%s#%s#%s#\n' % (rTag, rName, repr(rStack), repr(rHal), repr(rApp)))
    fd.close()
  except IOError:
    pass

#********************************************************************************
# Get record from cache.
#
# Parameters:
#   tag - tag of the required record
#   record - separated set of parameters of the required record
#
# Return:
#   File name from record with specified parameters or
#   None if no record found.
#
#********************************************************************************
def getRecord(tag, record):
  stack, hal, app = record
  for rTag, rName, rStack, rHal, rApp in __cacheRecords:
    if rTag == tag and rStack == stack and rHal == hal and rApp == app:
      return rName
  return None # Nothing found

#********************************************************************************
# Generate new unique name for cache file.
#
# Parameters:
#   none
#
# Return:
#   Unique file name.
#
#********************************************************************************
def getNewName():
  imageCachePath = env.getValue('imageCachePath')
  if imageCachePath:
    names = [rName for rTag, rName, rStack, rHal, rApp in __cacheRecords]
    newName = None
    while newName is None or newName in names:
      newName = str(int(random.random()*10000))
    return os.path.join(imageCachePath, newName)
  else:
    return tempfile.mktemp()

#********************************************************************************
# Put record to cache.
#
# Parameters:
#   name - file name associated with record
#   tag - tag of the record
#   record - separated set of parameters of the record
#
# Return:
#   none
#
#********************************************************************************
def putRecord(name, tag, record):
  global __cacheRecords
  # Look if record with requested parameters already exists
  cachedName = None
  stack, hal, app = record
  for rTag, rName, rStack, rHal, rApp in __cacheRecords:
    if rTag == tag and rStack == stack and rHal == hal and rApp == app:
      misc.removeFile(rName) # Free space for new record
      cachedName = rName

  if not cachedName: # Record is not found in cache
    cachedName = getNewName()
    __cacheRecords += [(tag, cachedName, stack, hal, app)] # Add new record

  try:
    shutil.copy(name, cachedName)
  except IOError:
    log.error('Can not copy application image file to temporary location', log = 'suite')
    # Erase record from cache
    for i in range(len(__cacheRecords)):
      rTag, rName, rStack, rHal, rApp = __cacheRecords[i]
      if rName == cachedName:
        __cacheRecords[i] = (None, None, None, None, None)
        break

#********************************************************************************
# Write cache to disk.
#
# Parameters:
#   none
#
# Return:
#   none
#
#********************************************************************************
def sync():
  imageCachePath = env.getValue('imageCachePath')
  if imageCachePath:
    writeRecords()
    return True
  else:
    return False

#********************************************************************************
# Sync cache and remove all temporary files.
#
# Parameters:
#   none
#
# Return:
#   none
#
#********************************************************************************
def cleanup():
  if not sync():
    for rTag, rName, rStack, rHal, rApp in __cacheRecords:
      misc.removeFile(rName)

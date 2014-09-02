
#********************************************************************************
# Exception used by check() to signal negative condition.
#********************************************************************************
class TestFailed(Exception):
  def __init__(self, msg, logName = None):
    self.__msg = msg
    self.__logger = logName

  def __str__(self):
    return 'Condition check failed: %s' % self.__msg

  def getMessage(self):
    return self.__msg

  def getLogger(self):
    return self.__logger

#********************************************************************************
# Exception used by freturn() to interrupt function execution.
#********************************************************************************
class FReturn(Exception):
  def __init__(self, ret):
    self.__ret = ret

  def getReturnValue(self):
    return self.__ret


def intToList(val, size):
  res = []
  for i in xrange(size):
    res = res + [val & 0xFF]
    val = val >> 8
  return res

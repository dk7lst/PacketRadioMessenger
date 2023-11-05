# General Tools & Helpers

import logging # https://docs.python.org/3/howto/logging.html

def logBuffer(prefix, buf):
  if logging.root.level > logging.DEBUG: return False
  debug = prefix + ": %d bytes: [" % len(buf)
  for bval in buf: debug += " %X" % bval
  debug += " ]"
  logging.debug(debug)
  return True

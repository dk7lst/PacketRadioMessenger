# General Tools & Helpers

import logging # https://docs.python.org/3/howto/logging.html

def toByte(value):
  return value.to_bytes(1, byteorder="little")

def logBuffer(prefix, buf):
  if logging.root.level > logging.DEBUG: return False
  debug = prefix + ": %d bytes: [" % len(buf)
  for bval in buf: debug += " %02X" % bval
  debug += " ]"
  logging.debug(debug)
  return True

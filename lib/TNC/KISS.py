import logging # https://docs.python.org/3/howto/logging.html
import lib
from . import AX25

# Class for KISS protocol implementation.
# https://en.wikipedia.org/wiki/KISS_(amateur_radio_protocol)
# https://www.ka9q.net/papers/kiss.html
class KISS:
  def __init__(self, config, section="KISS"):
    self.FEND = 0xC0 # Frame End
    self.FESC = 0xDB # Frame Escape
    self.TFEND = 0xDC # Transposed Frame End
    self.TFESC = 0xDD # Transposed Frame Escape
    self.ax25 = AX25.AX25(config, section)
    self.reset()

  def reset(self):
    self.framebuf = bytes()

  def processReceivedBytes(self, buf):
    lib.logBuffer("KISS: processReceivedBytes()", buf)
    for bval in buf:
      if bval == self.FEND:
        self.processReceivedFrame(self.framebuf)
        self.reset()
      self.framebuf += bval.to_bytes(1, byteorder="little")

  def processReceivedFrame(self, framebuf):
    lib.logBuffer("KISS: processReceivedFrame()", framebuf)
    if framebuf[0] != self.FEND:
      logging.debug("KISS: Protocol Violation: No valid/complete frame (not starting with FEND)")
      return False
    if len(framebuf) < 2: return True # Empty frames are allowed but to be ignored.
    if framebuf[1] & 0x0F != 0:
      logging.debug("KISS: Protocol Violation: TNC only allowed to send data frames to host")
      return False
    if framebuf[1] >> 4 != 0:
      logging.warning("KISS: Only 1 TNC supported at the moment, ignoring other channels.")
      return False

    framebuf = framebuf[2:] # Remove frame delimiter and command
    while True:
      pos = framebuf.find(self.FESC)
      if pos < 0: break # No escaped characters to translate.
      if pos + 1 >= len(framebuf):
        logging.debug("KISS: Protocol Violation: Frame must not end with FESC")
        return False
      bval = framebuf[pos + 1]
      if bval == self.TFEND: bval = self.FEND
      elif bval == self.TFESC: bval = self.FESC
      else:
        logging.debug("KISS: Protocol Violation: Illegal byte after FESC")
        return False
      framebuf = bval.to_bytes(1, byteorder="little") + framebuf[2:]
    if len(framebuf) > 0: self.ax25.processReceivedFrame(framebuf)
    return True

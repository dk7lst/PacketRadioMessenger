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

  def processReceivedBytes(self, buf, rxMsgQueue):
    lib.logBuffer("KISS: processReceivedBytes()", buf)
    for bval in buf:
      self.framebuf += lib.toByte(bval)
      if bval == self.FEND:
        msg = self.decodeFrame(self.framebuf)
        if msg != None: rxMsgQueue.put(msg)
        self.framebuf = lib.toByte(bval)

  def encodeFrame(self, cmd, data=None):
    return lib.toByte(self.FEND) + lib.toByte(cmd) + (self.escape(data) if data!=None else b"") + lib.toByte(self.FEND)

  def decodeFrame(self, frame):
    lib.logBuffer("KISS: decodeFrame()", frame)

    if len(frame) == 0: return None # Empty frames are allowed but to be ignored.

    if frame[0] != self.FEND:
      logging.debug("KISS: Protocol Violation: Frame not starting with FEND")
      return None

    if frame[-1] != self.FEND:
      logging.debug("KISS: Protocol Violation: Frame not ending with FEND")
      return None

    if len(frame) <= 2: return None # Empty frames are allowed but to be ignored.

    if frame[1] & 0x0F != 0:
      logging.debug("KISS: Protocol Violation: TNC only allowed to send data frames to host")
      return None

    if frame[1] >> 4 != 0:
      logging.warning("KISS: Only 1 TNC supported at the moment, ignoring other channels.")
      return None

    frame = self.unescape(frame[2:-1]) # Remove both frame delimiters and command, then unescape special bytes

    # Send frame to AX.25 decoder if non-empty:
    return self.ax25.decodeFrame(frame) if len(frame) > 0 else False

  def encodeMessage(self, msg):
    return self.encodeFrame(0x00, self.ax25.encodeFrame(msg))

  def leaveKissMode(self):
    return self.encodeFrame(0xFF)

  def escape(self, payload):
    buf = b""
    for bval in payload:
      if bval == self.FEND: buf += lib.toByte(self.FESC) + lib.toByte(self.TFEND)
      elif bval == self.FESC: buf += lib.toByte(self.FESC) + lib.toByte(self.TFESC)
      else: buf += lib.toByte(bval)
    return buf

  def unescape(self, payload):
    buf = b""
    idx = 0
    while idx < len(payload):
      bval = payload[idx]
      idx += 1
      if bval == self.FESC:
        if idx == len(payload):
          logging.debug("KISS: unescape(): Protocol Violation: Frame must not end with FESC")
          return None
        bval = payload[idx]
        idx += 1
        if bval == self.TFEND: bval = self.FEND
        elif bval == self.TFESC: bval = self.FESC
        else:
          logging.debug("KISS: unescape(): Protocol Violation: Illegal byte 0x%X after FESC at index %d" % (bval, idx))
          return None
      buf += lib.toByte(bval)
    return buf

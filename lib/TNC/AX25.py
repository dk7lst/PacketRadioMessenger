import logging # https://docs.python.org/3/howto/logging.html
import lib

# https://en.wikipedia.org/wiki/AX.25
# Spec: http://www.ax25.net/AX25.2.2-Jul%2098-2.pdf
# https://www.nordlink.org/data/uploads/downloads/TNN179.pdf
# AX.25 Frame Generator: https://notblackmagic.com/bitsnpieces/ax.25/

# Class for AX.25 protocol implementation.
# AX.25 is only used when TNC is in KISS-mode. In hostmode the AX.25 encoding/decoding is done by the TNC.
class AX25:
  def __init__(self, config, section="AX25"):
    logging.debug("Init class AX25")

  def processReceivedFrame(self, frame):
    lib.logBuffer("AX25: processReceivedFrame()", frame)

    addr = ""
    idx = 0
    while len(frame) > 0:
      bval = frame[0]
      frame = frame[1:]
      if idx % 7 < 6: addr += chr(bval >> 1)
      else: addr = "%s-%d;" % (addr.strip(), (bval >> 1) & 0xF) # TODO: Decode other bits
      if bval & 1: break
      idx += 1
    logging.debug('addr: "%s"' % addr)

    if len(frame) < 2: return # Too short! We need control (1 byte) + protocol identifier (1 byte) + info (payload, up to 256 bytes)
    ctrl = frame[0]
    logging.debug('ctrl: %X Frametype: %X' % (ctrl, ctrl & 3))
    if ctrl & 3 != 3: return # Ignore all but unnumbered frames (U frame)

    ProtocolIdentifier = frame[1] # Shouldn't be there for U-frames, but is?
    logging.debug('Protocol Identifier (PID): %X' % ProtocolIdentifier)

    payload = frame[2:]
    logging.debug('payload: "%s"' % payload)

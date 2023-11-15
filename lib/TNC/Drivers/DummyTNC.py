import logging # https://docs.python.org/3/howto/logging.html
import lib
from ..KISS import KISS
from ..AX25 import AX25

# Class for dummy TNC for testing.
class DummyTNC:
  def __init__(self, config, section, rxMsgQueue):
    logging.debug("Init class DummyTNC")
    self.rxMsgQueue = rxMsgQueue

    self.runTests(config, section) # Perform some self-tests

    self.kiss = KISS(config, section)
    self.kiss.processReceivedBytes(b"\xC0\x00\x88\x96\x6E\x98\xA6\xA8\x60\x88\x96\x6E\x98\xA6\xA8\xEF\x03\xF0\x54\x65\x73\x74\x0D\xC0", rxMsgQueue)

  def sendMessage(self, msg):
    logging.debug('DummyTNC: sendMessage(): %s' % msg)
    self.rxMsgQueue.put({"to": msg["from"], "from": msg["to"], "via": msg["via"].reverse(), "payload": msg["payload"]})

  def runTests(self, config, section):
    ax25 = AX25(config, section)
    self.compare(ax25.decodeAddressList(ax25.encodeAddress("abcd-7"))[0], ["ABCD-7"]) # Test callsign encoding
    self.compare(ax25.decodeAddressList(ax25.encodeAddressList("FROM-7", "TO", ["VIA-1", "VIA-2", "VIA-3"]))[0], ["TO", "FROM-7", "VIA-1", "VIA-2", "VIA-3"]) # Test callsign list encoding

    kiss = KISS(config, section)
    buf = b""
    for bval in range(0, 256): buf += lib.toByte(bval)
    escapedBuf = b""
    for bval in range(0, kiss.FEND): escapedBuf += lib.toByte(bval)
    escapedBuf += lib.toByte(kiss.FESC) + lib.toByte(kiss.TFEND)
    for bval in range(kiss.FEND + 1, kiss.FESC): escapedBuf += lib.toByte(bval)
    escapedBuf += lib.toByte(kiss.FESC) + lib.toByte(kiss.TFESC)
    for bval in range(kiss.FESC + 1, 256): escapedBuf += lib.toByte(bval)
    assert len(escapedBuf) == 256 + 2
    self.compare(kiss.escape(buf), escapedBuf)
    self.compare(kiss.unescape(escapedBuf), buf)

    msg = {"to": "TO-12", "from": "FROM", "via": ["VIA", "VIA-2"], "payload": b"This is my dummy payload!"}
    self.compare(kiss.decodeFrame(kiss.encodeMessage(msg)), msg)

  def compare(self, result, expected):
    if result == expected: return
    logging.debug('Test failed: result="%s" expected: "%s"' % (str(result), str(expected)))
    assert False

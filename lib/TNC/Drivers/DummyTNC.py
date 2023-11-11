import logging # https://docs.python.org/3/howto/logging.html
from ..KISS import KISS

# Class for dummy TNC for testing.
class DummyTNC:
  def __init__(self, config, section):
    logging.debug("Init class DummyTNC")
    kiss = KISS(config, section)
    kiss.processReceivedBytes(b"\xC0\x00\x88\x96\x6E\x98\xA6\xA8\x60\x88\x96\x6E\x98\xA6\xA8\xEF\x03\xF0\x54\x65\x73\x74\x0D\xC0")

import logging # https://docs.python.org/3/howto/logging.html
from ..KISS import KISS

# Class for dummy TNC for testing.
class DummyTNC:
  def __init__(self, config, section):
    logging.debug("Init class DummyTNC")
    kiss = KISS(config, section)
    kiss.processReceivedBytes(b"trash1\xC0\xC0\xC0\x00frame1\xC0\x00frame2\xC0trash2")

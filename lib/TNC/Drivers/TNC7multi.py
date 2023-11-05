import _thread
import logging # https://docs.python.org/3/howto/logging.html
from ..SerialBase import SerialBase
from ..KISS import KISS

# Class for TNC7multi TNC.
class TNC7multi(SerialBase):
  def __init__(self, config, section):
    logging.debug("Init class TNC7multi")
    super().__init__(config, section)
    self.kiss = KISS(config, section)
    _thread.start_new_thread(SerialReceiveThread, ())

  def SerialReceiveThread():
    while True: self.kiss.processReceivedBytes(self.getFrame())

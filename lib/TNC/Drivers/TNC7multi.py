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
    _thread.start_new_thread(self.SerialReceiveThread, ())

  def __del__(self, config, section):
    pass # TODO: Shutdown thread!

  def SerialReceiveThread(self):
    logging.debug("TNC7multi: SerialReceiveThread()")
    while True: self.kiss.processReceivedBytes(self.getFrame())

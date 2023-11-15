import _thread
import logging # https://docs.python.org/3/howto/logging.html
from ..SerialBase import SerialBase
from ..KISS import KISS

# Class for TNC7multi TNC.
class TNC7multi(SerialBase):
  def __init__(self, config, section, rxMsgQueue):
    logging.debug("Init class TNC7multi")
    super().__init__(config, section)
    self.kiss = KISS(config, section)
    _thread.start_new_thread(self.SerialReceiveThread, (rxMsgQueue,))

  def __del__(self, config, section):
    pass # TODO: Shutdown thread!

  def sendMessage(self, msg):
    self.sendFrame(self.kiss.encodeMessage(msg))

  def SerialReceiveThread(self, rxMsgQueue):
    logging.debug("TNC7multi: SerialReceiveThread()")
    while True: self.kiss.processReceivedBytes(self.getFrame(), rxMsgQueue)

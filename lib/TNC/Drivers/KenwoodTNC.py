import logging # https://docs.python.org/3/howto/logging.html
from ..SerialBase import SerialBase
from ..KISS import KISS

# Class for Kenwood TNCs (TM-D700, TM-D710, TH-D72, TH-D74, TH-D75, ...).
class KenwoodTNC(SerialBase):
  def __init__(self, config, section):
    logging.debug("Init class KenwoodTNC")
    super().__init__(config, section)
    self.kiss = KISS(config, section)
    _thread.start_new_thread(self.SerialReceiveThread, ())

  def __del__(self, config, section):
    self.sendFrame(self.kiss.encodeLeaveKissMode())
    pass # TODO: Shutdown thread!

  def SerialReceiveThread(self):
    logging.debug("KenwoodTNC: SerialReceiveThread()")
    while True: self.kiss.processReceivedBytes(self.getFrame())

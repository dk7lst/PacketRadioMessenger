import _thread
import logging # https://docs.python.org/3/howto/logging.html
from .Drivers.DummyTNC import DummyTNC
from .Drivers.KenwoodTNC import KenwoodTNC
from .Drivers.TNC7multi import TNC7multi

# Class for access to Terminal Node Controller (TNC).
class TNC:
  def __init__(self, config, txMsgQueue, rxMsgQueue):
    logging.debug("Init class TNC")
    self.tncList = []
    if config.getBool("DummyTNC", "enabled"): self.tncList.append(DummyTNC(config, "DummyTNC", rxMsgQueue))
    else: # Don't mix Dummy-TNC with real TNCs to avoid sending test data on real frequencies
      if config.getBool("KenwoodTNC", "enabled"): self.tncList.append(KenwoodTNC(config, "KenwoodTNC", rxMsgQueue))
      if config.getBool("TNC7multi", "enabled"): self.tncList.append(TNC7multi(config, "TNC7multi", rxMsgQueue))
    if len(self.tncList) == 0: logging.warning("TNC: No TNC driver enabled in config file!")
    _thread.start_new_thread(self.RouteThread, (txMsgQueue,))

  def __del__(self, config, section):
    pass # TODO: Shutdown thread!

  # Forward messages to active TNCs.
  # For now, send all messages to all TNCs. Maybe implement some sort of routing later?
  def RouteThread(self, txMsgQueue):
    logging.debug("TNC: RouteThread()")
    while True:
      msg = txMsgQueue.get()
      logging.debug("TNC: RouteThread(): Forwarding " + str(msg))
      for tnc in self.tncList: tnc.sendMessage(msg)

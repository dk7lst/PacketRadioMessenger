import logging # https://docs.python.org/3/howto/logging.html
from .Drivers.DummyTNC import DummyTNC
from .Drivers.KenwoodTNC import KenwoodTNC
from .Drivers.TNC7multi import TNC7multi

# Class for access to Terminal Node Controller (TNC)
class TNC:
  def __init__(self, config):
    logging.debug("Init class TNC")
    self.tncList = []
    if config.getBool("DummyTNC", "enabled"): self.tncList.append(DummyTNC(config, "DummyTNC"))
    if config.getBool("KenwoodTNC", "enabled"): self.tncList.append(KenwoodTNC(config, "KenwoodTNC"))
    if config.getBool("TNC7multi", "enabled"): self.tncList.append(TNC7multi(config, "TNC7multi"))

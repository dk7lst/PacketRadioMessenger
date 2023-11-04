import logging # https://docs.python.org/3/howto/logging.html
from .SerialBase import SerialBase

# Class for Kenwood TNCs (TM-D700, TM-D710, TH-D72, TH-D74, TH-D75, ...)
class KenwoodTNC(SerialBase):
  def __init__(self, config, section):
    logging.debug("Init class KenwoodTNC")
    super().__init__(config, section)

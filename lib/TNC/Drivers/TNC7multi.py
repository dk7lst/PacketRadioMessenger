import logging # https://docs.python.org/3/howto/logging.html
from ..SerialBase import SerialBase

# Class for TNC7multi TNC
class TNC7multi(SerialBase):
  def __init__(self, config, section):
    logging.debug("Init class TNC7multi")
    super().__init__(config, section)

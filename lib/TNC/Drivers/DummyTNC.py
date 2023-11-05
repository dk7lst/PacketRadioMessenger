import logging # https://docs.python.org/3/howto/logging.html

# Class for dummy TNC for testing.
class DummyTNC:
  def __init__(self, config, section):
    logging.debug("Init class DummyTNC")

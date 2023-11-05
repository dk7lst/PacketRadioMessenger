import logging # https://docs.python.org/3/howto/logging.html
import lib

# Class for AX.25 protocol implementation.
# AX.25 is only used when TNC is in KISS-mode. In hostmode the AX.25 encoding/decoding is done by the TNC.
# https://en.wikipedia.org/wiki/AX.25
# The Cyclic Redundancy Check (CRC) for AX.25: http://practicingelectronics.com/articles/article-100003/article.php
class AX25:
  def __init__(self, config, section="AX25"):
    logging.debug("Init class AX25")

  def processReceivedFrame(self, frame):
    lib.logBuffer("AX25: processReceivedFrame()", frame)

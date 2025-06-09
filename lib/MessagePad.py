import math
import curses # https://docs.python.org/3/howto/curses.html https://docs.python.org/3/library/curses.html
import logging # https://docs.python.org/3/howto/logging.html

# Class for storing messages and rendering a timeline-view to a curses pad/window.
class MessagePad:
  def __init__(self, config):
    self.config = config
    self.msgList = {} # Dict with timecode-Key to have list sorted and allow for easy access.
    self.needsUpdateFlag = True

  def needsUpdate(self):
    return self.needsUpdateFlag

  def requestUpdate(self):
    self.needsUpdateFlag = True

  def addMessage(self, msg, outgoing):
    msg["outgoing"] = outgoing
    self.msgList[msg["id"]] = msg
    self.needsUpdateFlag = True

  def render(self, pad):
    y = 0
    pad.erase()
    for id, msg in self.msgList.items():
      pad.addstr(y, 0, msg["text"], curses.color_pair(1) if msg["outgoing"] else curses.color_pair(2))
      y += math.ceil(len(msg["text"]) / pad.getmaxyx()[1])
    self.needsUpdateFlag = False

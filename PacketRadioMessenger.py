#!/bin/python3
import curses # https://docs.python.org/3/howto/curses.html https://docs.python.org/3/library/curses.html
import curses.textpad
import argparse # https://docs.python.org/3/library/argparse.html
import logging # https://docs.python.org/3/howto/logging.html
import lib.Config
import lib.Protocol
import lib.MessagePad

def HighlightWindow(windowList, idx):
  for w in windowList:
    w.bkgd(' ', curses.color_pair(2 if w == windowList[idx] else 0))
    w.refresh()

def main(stdscr):
  # Clear screen:
  stdscr.clear()
  stdscr.refresh()

  # Define colors:
  curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

  # Create upper left window displaying the contact list:
  contactcols = config.getInt("ui", "contactcols", 14)
  contactwin = stdscr.subwin(curses.LINES - 3, contactcols, 0, 0) # height, width, begin_y, begin_x
  contactwin.border()
  contactwin.addstr(0, 2, "[Contacts]")
  contactwin.refresh()

  # Create upper right window displaying the message timeline:
  listwin = stdscr.subwin(curses.LINES - 3, curses.COLS - contactcols, 0, contactcols) # height, width, begin_y, begin_x
  listwin.border()
  listwin.addstr(0, 2, "[Messages]")
  listwin.refresh()

  # Create lower window to input new messages:
  inputwin = stdscr.subwin(3, curses.COLS, curses.LINES - 3, 0)
  inputwin.border()
  inputwin.addstr(0, 2, "[Enter Message]")
  inputwin.refresh()

  # Create edit window inside lower window:
  editwin = inputwin.subwin(1, curses.COLS - 2, curses.LINES - 2, 1)
  editwin.bkgdset(' ', curses.color_pair(2)) # Text always uses active window color
  editwin.timeout(250) # set timeout for getch() in ms.
  tb = curses.textpad.Textbox(editwin, insert_mode=True)

  # Create virtual pad with actual timeline to be displayed inside upper right window.
  # Can hold more lines than actual fit on the screen so user scan scroll up/down.
  listpad = curses.newpad(config.getInt("ui", "messagelines", 100), listwin.getmaxyx()[1] - 2)

  # List for window highlighting when pressing TAB key:
  windowTabOrderList = [inputwin, contactwin, listwin]
  activeWindowIdx = 0
  HighlightWindow(windowTabOrderList, activeWindowIdx)
  messageWindowScrollY = 0

  while True:
    if mpad.needsUpdate():
      # Render timeline to curses-pad and redraw screen:
      #y, x = curses.getsyx()
      mpad.render(listpad)
      listpad.refresh(messageWindowScrollY, 0, listwin.getbegyx()[0] + 1, listwin.getbegyx()[1] + 1, listwin.getbegyx()[0] + listwin.getmaxyx()[0] - 2, listwin.getbegyx()[1] + listwin.getmaxyx()[1] - 2) # pad_y, pad_x, screen_y1, screen_x1, screen_y2, screen_x2
      #curses.setsyx(y, x)
    ch = editwin.getch()
    if ch == 27: break # ESC to exit
    if ch == 9: # TAB to switch windows
      activeWindowIdx = (activeWindowIdx + 1) % len(windowTabOrderList)
      HighlightWindow(windowTabOrderList, activeWindowIdx)
      mpad.requestUpdate()
    elif activeWindowIdx == 0: # Keys for input window
      if ch == 10: # ENTER to send message
        msgtext = tb.gather().strip()
        prot.sendMessage(msgtext)
        tb.do_command(curses.ascii.SOH)
        tb.do_command(curses.ascii.VT)
        listwin.refresh()
      else: tb.do_command(ch)
    elif activeWindowIdx == 2: # Keys for message window
      if ch == curses.KEY_UP:
        messageWindowScrollY = max(messageWindowScrollY - 1, 0)
        mpad.requestUpdate()
      elif ch == curses.KEY_DOWN:
        messageWindowScrollY = min(messageWindowScrollY + 1, listpad.getmaxyx()[0] - listwin.getmaxyx()[0] + 2)
        mpad.requestUpdate()

# Command line parsing:
parser = argparse.ArgumentParser(prog="PacketRadioMessenger",
  description="Simple messenger for chatting via ham-radio packet radio.")
parser.add_argument("-c", "--conf", default="PacketRadioMessenger.ini", help="Specify config file.")
args = parser.parse_args()

# Load config file:
config = lib.Config.Config(args.conf)

# Initialize logger:
loglevel = getattr(logging, config.getString("general", "loglevel", "WARNING").upper(), None)
if not isinstance(loglevel, int):
  print("Unknown log level in config! Use one of DEBUG, INFO, WARNING, ERROR, CRITICAL!")
  exit(1)
logging.basicConfig(filename=config.getString("general", "logfile", "PacketRadioMessenger.log"), format='%(asctime)s %(levelname)s: %(message)s', level=loglevel)
logging.info("APP START")

callsign = config.getCallsign()
if len(callsign) == 0 or callsign == "CHANGEME":
  print("Please set callsign in config file!")
  exit(1)

mpad = lib.MessagePad.MessagePad(config)
prot = lib.Protocol.Protocol(config, mpad)

curses.wrapper(main)
logging.info("APP EXIT")

#!/bin/python3
import curses # https://docs.python.org/3/howto/curses.html https://docs.python.org/3/library/curses.html
import curses.textpad
import logging # https://docs.python.org/3/howto/logging.html
import lib.Config
import lib.Protocol
import lib.MessagePad

def main(stdscr):
  stdscr.clear()
  stdscr.refresh()

  # Define colors:
  curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

  # Create upper window displaying the message timeline:
  listwin = stdscr.subwin(curses.LINES - 3, curses.COLS, 0, 0) # height, width, begin_y, begin_x
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
  editwin.timeout(250) # set timeout for getch()
  tb = curses.textpad.Textbox(editwin, insert_mode=True)

  # Create virtual pad with actual timeline to be displayed inside upper window.
  # Can hold more lines than actual fit on the screen so user scan scroll up/down.
  listpad = curses.newpad(config.getInt("ui", "messagelines", 100), curses.COLS - 2)

  while True:
    if mpad.needsUpdate():
      # Render timeline to curses-pad and redraw screen:
      #y, x = curses.getsyx()
      mpad.render(listpad)
      listpad.refresh(0, 0, 1, 1, curses.LINES - 5, curses.COLS - 1) # pad_y, pad_x, screen_y1, screen_x1, screen_y2, screen_x2
      #curses.setsyx(y, x)
    ch = editwin.getch()
    if ch == 27: break # ESC
    elif ch == 10: # ENTER
      msgtext = tb.gather().strip()
      prot.sendMessage(msgtext)
      tb.do_command(curses.ascii.SOH)
      tb.do_command(curses.ascii.VT)
      #editwin.clear()
      listwin.refresh()
    else: tb.do_command(ch)

# Load config file:
config = lib.Config.Config("PacketRadioMessenger.ini")

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

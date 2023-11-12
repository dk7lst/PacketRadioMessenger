#!/bin/python3
import curses # https://docs.python.org/3/howto/curses.html https://docs.python.org/3/library/curses.html
import curses.textpad
import logging # https://docs.python.org/3/howto/logging.html
import lib.Config
import lib.Protocol

def main(stdscr):
  stdscr.clear()
  stdscr.refresh()

  listwin = curses.newwin(curses.LINES - 3, curses.COLS, 0, 0) # height, width, begin_y, begin_x
  listwin.border()
  listwin.addstr(0, 2, "[Messages]")
  listwin.refresh()

  inputwin = curses.newwin(3, curses.COLS, curses.LINES - 3, 0)
  inputwin.border()
  inputwin.addstr(0, 2, "[Enter Message]")
  inputwin.refresh()

  editwin = curses.newwin(1, curses.COLS - 2, curses.LINES - 2, 1)
  tb = curses.textpad.Textbox(editwin, insert_mode=True)
  #tb.edit()
  while True:
    ch = editwin.getch()
    if ch == 27: break # ESC
    elif ch == 10: # ENTER
      msgtext = tb.gather().strip()
      listwin.addstr(1, 1, "Test: " + msgtext)
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

prot = lib.Protocol.Protocol(config)

curses.wrapper(main)
logging.info("APP EXIT")

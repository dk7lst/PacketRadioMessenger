#!/bin/python3
import curses # https://docs.python.org/3/howto/curses.html https://docs.python.org/3/library/curses.html
import curses.textpad

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
    if ch == 27: break
    elif ch == 10:
      listwin.addstr(1, 1, "Test: " + tb.gather().strip())
      tb.do_command(curses.ascii.SOH)
      tb.do_command(curses.ascii.VT)
      #editwin.clear()
      listwin.refresh()
    else: tb.do_command(ch)
  #curses.curs_set(False) # Hide cursor

curses.wrapper(main)

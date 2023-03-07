#!/usr/bin/python3
from sys import argv
import curses
from curses import wrapper

def main(stdscr):
    stdscr.nodelay(True)
    snake = [tuple(int(i/2) for i in stdscr.getmaxyx())]
    while True:
        for part in snake:
            stdscr.addstr(*part, '#')
        c = stdscr.getch()
        if c == ord('a'):
            break
        elif c == ord('s'):
            break
        elif c == ord('w'):
            break
        elif c == ord('d'):
            break
    stdscr.nodelay(False)
    pos = list(int(i/2) for i in stdscr.getmaxyx())
    pos[1] -= 5
    stdscr.addstr(*pos, 'GAME OVER!')
    stdscr.getch()


wrapper(main)

#!/usr/bin/python3
from sys import argv
import curses
from curses import wrapper
from random import randint

@wrapper
def main(stdscr):
    stdscr.nodelay(True)
    y, x = stdscr.getmaxyx()
    snake = [[int(y/2), int(x/2)]]
    apple = [randint(1, y), randint(1, x)]
    dir = [0, 0]
    while True:
        stdscr.clear()
        c = stdscr.getch()
        if c == ord('a'):
            dir[0] = -1
        elif c == ord('s'):
            dir[1] = -1
        elif c == ord('w'):
            dir[1] = 1
        elif c == ord('d'):
            dir[0] = 1
        elif c == ord(' '):
            break
        snake[0][0] += dir[0]
        snake[0][1] += dir[1]
        for part in snake:
            stdscr.addstr(*part, '#')
        stdscr.addstr(*apple, '@')
    stdscr.nodelay(False)
    pos = list(int(i/2) for i in stdscr.getmaxyx())
    pos[1] -= 5
    stdscr.addstr(*pos, 'GAME OVER!')
    stdscr.getch()

#!/usr/bin/python3
from tkinter import Tk
import config
from sys import argv
from yoi import *


def main():
    win = Tk()
    win.title('Yoi')
    win.geometry('1560x720')
    m = Yoi(win, path=(argv[1] if len(argv) > 1 else ''))
    m.pack(fill='both', expand=True)
    win.mainloop()


if __name__ == '__main__':
    main()


#!/usr/bin/python3
from tkinter import Tk
import config
from sys import argv
from yoi import *


def main():
    cfg = dict((k, config.__dict__[k]) for k in list(
        config.__dict__.keys()) if not k.startswith('__'))
    win = Tk()
    win.title('Yoi')
    win.geometry('1440x720')
    m = Yoi(win, path=(argv[1] if len(argv) > 1 else ''), **cfg)
    m.pack(fill='both', expand=True)
    win.mainloop()


if __name__ == '__main__':
    main()

#!/usr/bin/python3
from sys import argv
from os import *
from os.path import *
from tkinter import Tk
import config
from yoi import *


def main():
    [__import__(f'plugins.{path}') for path in listdir('src/plugins')]
    cfg = dict((k, config.__dict__[k]) for k in list(
        config.__dict__.keys()) if not k.startswith('__'))
    win = Tk()
    win.title('Yoi')
    m = Yoi(win, path=(argv[1] if len(argv) > 1 else ''), **cfg)
    m.pack(fill='both', expand=True)
    win.mainloop()


if __name__ == '__main__':
    main()

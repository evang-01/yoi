from tkinter import Label
from yoi.folder import Folder
from os import listdir
from os.path import basename


class FileManager(Folder):
    def __init__(self, root, path='', ifisfile=lambda name: None,
                 bg='#000', dc='#f0f', fc='#0f0', oc='#0ff',
                 indent=32, font=('Courier', 4, 'bold')):
        super().__init__(root)
        self.path = path
        self.open(path=path, ifisfile=ifisfile)
        self.name.destroy()
        self.name = Label(self, text=basename(path).upper(),
                          font=font, width=indent, bg=bg, fg=oc)
        self.elems = []

        self.indent = indent
        self.font = font
        self.bg = bg
        self.fc = fc
        self.dc = dc

    def display(self):
        self.name.config(text=self.name['text'].upper())
        self.name.pack(ipady=16)
        for el in self.elems:
            el.pack(padx=(0, 0), anchor='w')

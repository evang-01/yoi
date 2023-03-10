from tkinter import Frame, Button
from os import listdir
from os.path import isfile, join, abspath, basename


class Folder(Frame):
    def __init__(self, root, path='', ifisfile=lambda name: None, bg='#000', dc='#f0f', fc='#0f0', oc='#0ff', width=32, indent=128, font=('Courier', 4, 'bold')):
        super().__init__(root, bg=bg)
        self.path = path
        self.name = Button(self, text=basename(path), width=width, font=font,
                           bg=bg, fg=fc if isfile(path) else dc, command=lambda: self.open())
        self.name.pack(anchor='w')
        self.elems = []

        self.width = width
        self.indent = indent
        self.ifisfile = ifisfile
        self.font = font
        self.bg = bg
        self.fc = fc
        self.dc = dc

    def display(self):
        self.name.pack(ipady=0)
        self.name.config(text=basename(self.path))
        for el in self.elems:
            el.pack(padx=(self.indent, 0), anchor='w')

    def open(self, path=''):
        path = self.path if path == '' else path
        if isfile(path):
            self.ifisfile(path)
            return
        for elem in self.elems:
            path = ''
            elem.destroy()
        self.elems.clear()
        if path == '':
            return
        for elem in listdir(abspath(path)):
            def iffile(path=join(path, elem)): return self.ifisfile(path)
            if isfile(elem):
                self.elems.append(Button(
                    self, text=elem, font=self.font, width=self.width, bg=self.bg, fg=self.fc))
                self.elems[-1]['command'] = iffile
            else:
                folder = Folder(self, path=join(path, elem), ifisfile=iffile, width=self.width,
                                indent=self.indent, font=self.font, bg=self.bg, fc=self.fc, dc=self.dc)
                self.elems.append(folder)
        self.path = path
        self.display()

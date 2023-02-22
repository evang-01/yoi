from tkinter import Frame, Button
from os import listdir
from os.path import isfile, join, abspath, basename


class Folder(Frame):
    def __init__(self, root, path='', ifisfile=lambda name: None,
                 bg='#000', dc='#f0f', fc='#0f0', oc='#0ff',
                 indent=32, font=('Courier', 4, 'bold')):
        super().__init__(root, bg=bg)
        self.path = path
        self.name = Button(self, text=basename(path), width=indent, font=font,
                           bg=bg, fg=fc if isfile(path) else dc,
                           command=lambda: self.open(ifisfile=ifisfile))
        self.name.pack(anchor='w')
        self.elems = []

        self.indent = indent
        self.font = font
        self.bg = bg
        self.fc = fc
        self.dc = dc

    def display(self):
        self.name.pack(ipady=0)
        for el in self.elems:
            el.pack(padx=(self.indent*self.font[1]/2, 0), anchor='w')

    def open(self, path='', ifisfile=lambda name: None):
        path = self.path if path == '' else path
        self.name.config(text=basename(path))
        if isfile(path):
            ifisfile(path)
            return
        for elem in self.elems:
            path = ''
            elem.destroy()
        self.elems.clear()
        if path == '':
            return
        for elem in listdir(abspath(path)):
            def iffile(path=elem): return ifisfile(path)
            if isfile(elem):
                self.elems.append(Button(self, text=elem, font=self.font,
                                         width=self.indent, bg=self.bg, fg=self.fc))
                self.elems[-1]['command'] = iffile
            else:
                folder = Folder(self, path=join(path, elem), ifisfile=iffile,
                                indent=self.indent, font=self.font, bg=self.bg,
                                fc=self.fc, dc=self.dc)
                self.elems.append(folder)
        self.display()

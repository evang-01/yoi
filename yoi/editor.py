from tkinter import Text
from os.path import basename
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re


class Editor(Text):
    def __init__(self, root=None, path='', tags={}, **kwargs):
        super().__init__(root, **kwargs)
        self.path = path
        self.tags = tags
        self.bind('<KeyRelease>', lambda _: self.save())
        self.open(path=path)

    def open(self, path=''):
        self.path = path
        self.delete('1.0', 'end')
        self['state'] = 'disabled'
        if path != '':
            self['state'] = 'normal'
            with open(path, 'r') as file:
                self.insert('1.0', file.read())
        self.syntax()

    def syntax(self):
        if basename(self.path).split('.')[-1] == 'py':
            return
        '''cdg = ic.ColorDelegator()
        cdg.prog = re.compile(r'\b(?P<MYGROUP>tkinter)\b|' + ic.make_pat(), re.S)
        cdg.idprog = re.compile(r'\s+(\w+)', re.S)
        cdg.tagdefs = self.tags
        ip.Percolator(self).insertfilter(cdg)'''

    def save(self):
        if self.path != '':
            with open(self.path, 'w') as file:
                file.write(self.get('1.0', 'end'))

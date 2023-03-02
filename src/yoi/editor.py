from tkinter import Text
from os.path import basename
from pygments import lex
from pygments.lexers import *
from pygments.token import Token


class Editor(Text):
    def __init__(self, root=None, path='', tags={
        'builtin': '#0f0',
        'name': '#fff',
        'comment': '#00f',
        'keyword': '#f0f',
        'literal': '#ff0',
        'punctuation': '#f00',
        'operator': '#0ff'
    }, lexer=PythonLexer(), **kwargs):
        super().__init__(root, **kwargs)
        self.path = path
        self.tags = tags
        self.lexer = lexer
        for tag, color in tags.items():
            self.tag_configure(tag, foreground=color, selectforeground=kwargs['fg'] if color ==
                               kwargs['selectbackground'] else color, selectbackground=kwargs['selectbackground'])
        self.bind('<KeyRelease>', lambda _: self.save())
        self['state'] = 'disable'
        self.open(path=path)

    def open(self, path=''):
        self.path = path
        self.delete('1.0', 'end')
        self.code = ''
        self['state'] == 'disable'
        if path != '':
            self['state'] = 'normal'
            with open(path, 'r') as file:
                self.code = file.read()
        self.save()

    def syntax(self):
        tokens = self.lexer.get_tokens(self.code)
        sl = 1
        sr = 0
        el = 1
        er = 0
        for tag, val in tokens:
            if "\n" in val:
                el += val.count("\n")
                er = len(val.rsplit("\n", 1)[1])
            else:
                er += len(val)
            if val not in (" ", "\n"):
                begin = f"{sl}.{sr}"
                end = f"{el}.{er}"
                for old in self.tag_names():
                    self.tag_remove(old, begin, end)
                for newtag in self.tags:
                    tag = str(tag).replace('Token.', '').lower().\
                        replace('.', ' ').replace('namespace', 'library')
                    if newtag in tag or tag in newtag:
                        tag = newtag
                self.tag_add(tag, begin, end)
            sl = el
            sr = er

    def save(self):
        if self.path != '':
            with open(self.path, 'w') as file:
                file.write(self.code)
        self.syntax()

    @property
    def code(self):
        return self.get('1.0', 'end')

    @code.setter
    def code(self, code=''):
        if code != '':
            while code[-1] == '\n':
                code = code[:-1]
        code += '\n'
        self.delete('1.0', 'end')
        self.insert('1.0', code if code != None else '')


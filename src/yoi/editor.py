from tkinter import Text
from os.path import basename
from pygments import lex
from pygments.lexers import *
from pygments.token import Token


class Editor(Text):
    def __init__(self, root=None, path='', tags={
        'Name': '#0f0',
        'Comment': '#00f',
        'Keyword': '#f0f',
        'Literal': '#ff0',
        'Punctuation': '#f00',
        'Operator': '#0ff'
    }, **kwargs):
        super().__init__(root, **kwargs)
        self.path = path
        for tag, color in tags.items():
            self.tag_configure(tag, foreground=color, background=dict(**kwargs)['bg'])
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
        tokensource = PythonLexer().get_tokens(self.code)
        sl = 1
        sr = 0
        el = 1
        er = 0
        for tag, val in tokensource:
            if "\n" in val:
                el += val.count("\n")
                er = len(val.rsplit("\n",1)[1])
            else:
                er += len(val)
            if val not in (" ", "\n"):
                begin = f"{sl}.{sr}"
                end = f"{el}.{er}"
                for old in self.tag_names():
                    self.tag_remove(old, begin, end)
                self.tag_add(str(tag)[6:], begin, end)
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
    def code(self, code: str | list):
        if isinstance(code, list):
            code = '\n'.join(code)
        if code != '':
            while code[-1] == '\n':
                code = code[:-1]
        code += '\n'
        self.delete('1.0', 'end')
        self.insert('1.0', code if code != None else '')


from tkinter import Text
from pygments.lexers import PythonLexer
from pygments.lexers import *


class Editor(Text):
    def __init__(self, root=None, path='', tags={
        'builtin': '#0f0',
        'class': '#0f0',
        'function': '#0f0',
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
        self.history = ['']
        self.hist_index = 0
        self.on_save = lambda: None
        for tag, color in tags.items():
            self.tag_configure(tag, foreground=color, selectforeground=kwargs['fg'] if color ==
                               kwargs['selectbackground'] else color, selectbackground=kwargs['selectbackground'])
        self.bind('<KeyRelease>', self.save)
        self.bind('<Control-z>', self.undo)
        self.bind('<Control-y>', self.redo)
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
        self.history = [self.code]
        self.hist_index = 0
        self.on_save()
        self.syntax()
        self.save()

    def undo(self, *args):
        if self.hist_index > 0:
            self.hist_index -= 1
            self.code = self.history[self.hist_index]
        self.on_save()
        self.syntax()
        self.save()

    def redo(self, *args):
        if self.hist_index < len(self.history) - 1:
            self.hist_index += 1
            self.code = self.history[self.hist_index]
        self.on_save()
        self.syntax()
        self.save()

    def save(self, *args):
        if self.path != '':
            with open(self.path, 'w') as file:
                file.write(self.code[:-1])
        if self.code != self.history[self.hist_index]:
            self.on_save()
            self.syntax()
            if self.hist_index < len(self.history) - 1:
                if self.code != self.history[self.hist_index+1]:
                    del self.history[self.hist_index+1:]
                    self.hist_index = len(self.history) - 1
            self.history.append(self.code)
            self.hist_index += 1

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
                mi = 0
                tag = str(tag).replace('Token.', '').lower().split('.')
                for newtag in self.tags:
                    if newtag in tag:
                        i = tag.index(newtag)
                        if i > mi:
                            mi = i
                tag = tag[mi]
                self.tag_add(tag, begin, end)
            sl = el
            sr = er

    @property
    def code(self):
        return self.get('1.0', 'end')

    @code.setter
    def code(self, code=''):
        if code != '':
            while code[-1] == '\n':
                code = code[:-1]
        self.delete('1.0', 'end')
        self.insert('1.0', code)

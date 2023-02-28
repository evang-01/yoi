from tkinter import Text
from os.path import basename
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token


class Editor(Text):
    def __init__(self, root=None, path='', tags={
        'Name': '#0f0',
        'Comment': '#00f',
        'Keyword': '#f0f',
        'Literal': '#ff0',
        'Punctuation': '#f00'
    }, **kwargs):
        super().__init__(root, **kwargs)
        self.path = path
        for tag, color in tags.items():
            self.tag_configure(tag, foreground=color, background=dict(**kwargs)['bg'])
        self.bind('<KeyRelease>', lambda _: self.save())
        self.open(path=path)

    def open(self, path=''):
        self.path = path
        self.delete('1.0', 'end')
        self.code = ''
        if path != '':
            self['state'] = 'normal'
            with open(path, 'r') as file:
                self.code = file.read()
        self.save()

    def syntax(self):
        tokensource = PythonLexer().get_tokens(self.code)
        start_line=1
        start_index = 0
        end_line=1
        end_index = 0
        
        for ttype, value in tokensource:
            if "\n" in value:
                end_line += value.count("\n")
                end_index = len(value.rsplit("\n",1)[1])
            else:
                end_index += len(value)
 
            if value not in (" ", "\n"):
                index1 = "%s.%s" % (start_line, start_index)
                index2 = "%s.%s" % (end_line, end_index)
 
                for tagname in self.tag_names():
                    self.tag_remove(tagname, index1, index2)
 
                self.tag_add(str(ttype).split('.')[1], index1, index2)
 
            start_line = end_line
            start_index = end_index

    def save(self):
        if self.path != '':
            with open(self.path, 'w') as file:
                file.write(self.code)
        self.syntax()

    @property
    def code(self):
        return self.get('1.0', 'end')

    @code.setter
    def code(self, code: str | list | None):
        if isinstance(code, list):
            code = '\n'.join(code)
        self.delete('1.0', 'end')
        self.insert('1.0', code if code != None else '')

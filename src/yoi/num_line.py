from tkinter import Text
from yoi.editor import Editor


class NumLine(Text):
    def __init__(self, root, editor: Editor, bg='#000', fg='#fff', font=('Courier', 16, 'bold')):
        super().__init__(root, bg=bg, fg=fg, font=font)
        self.editor = editor
        self.editor.on_save = self.numerate
        self.numerate()

    def numerate(self, *args):
        self['state'] = 'normal'
        self.delete('1.0', 'end')
        lines = self.editor.code.count('\n')
        text = '\n'.join([str(i) for i in range(1, lines + 1)])
        self.insert('1.0', text)
        self['width'] = len(str(lines))
        self['state'] = 'disable'
        self.yview('moveto', self.editor.yview()[0])

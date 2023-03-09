from tkinter import Frame, Button
from yoi.editor import Editor
from os.path import basename, isfile


class FileList(Frame):
    def __init__(self, root, editor: Editor, button: Button, bg='#000', oc='#0ff', font=('Courier', 16, 'bold')):
        super().__init__(root, bg=bg)
        self.opened = dict()
        self.bg = bg
        self.oc = oc
        self.font = font
        self.editor = editor
        self.button = button

    def open(self, path='', use_path=False):
        if path == '' or not isfile(path) or path in self.opened:
            return
        self.button.forget()
        file = Frame(self, bg=self.bg)
        Button(file, text=path if use_path else basename(path), bg=self.bg, fg=self.oc,
               font=self.font, command=lambda f=path: self.editor.open(f)).pack(side='left')
        Button(file, text='x', bg=self.bg, fg='#f00', font=self.font,
               command=lambda f=path: self.close(f)).pack(side='right')
        file.pack(side='right')
        self.opened[path] = file

    def close(self, path):
        self.opened[path].destroy()
        del self.opened[path]
        last = list(self.opened.keys())[-1] if self.opened != {} else ''
        if self.opened == {}:
            self.button.pack()
            self.editor.open('')
            self.editor['state'] = 'disabled'
        self.editor.open(last)

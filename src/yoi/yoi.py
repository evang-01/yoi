from os import system
from os.path import isfile, isdir, basename, abspath
from tkinter import Frame, Scrollbar, Button
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.font import Font
from yoi import *


class Yoi(Frame):
    def __init__(self, root, path='', bg='#000', fg='#fff', dc='#f0f', fc='#0f0', width=1560, height=720, tags={
            'builtin': '#0f0',
            'class': '#0f0',
            'function': '#0f0',
            'comment': '#00f',
            'keyword': '#f0f',
            'literal': '#ff0',
            'punctuation': '#f00',
            'operator': '#0ff'
    }, fw=32, oc='#0ff', sg='#00f', ac='#0f0', font=('Courier', 12, 'bold'), indent=16, tabs=4):
        super().__init__(root, width=width, height=height)
        self.sg = sg
        self.bg = bg
        self.oc = oc
        self.font = font
        self.config(bg=bg)

        self.file_manager = FileManager(self, bg=bg, oc=oc, font=font, width=fw,
                                        fc=fc, dc=dc, indent=indent, ifisfile=lambda file: self.open_file(file))
        self.open_folder_btn = Button(
            self.file_manager, bg=bg, fg=dc, font=font, text='OPEN FOLDER', command=lambda: self.open_folder())
        self.open_folder_btn.pack()

        self.scrolly = Scrollbar(
            self, orient='vertical', bg=ac, activebackground=fg, troughcolor=bg)
        self.editor = Editor(self, path='', tags=tags, bg=bg, insertbackground=fg, tabs=Font(font=font).measure(
            ' ' * tabs), selectbackground=sg, selectforeground=fg, inactiveselectbackground=sg, fg=fg, font=font)
        self.open_file_btn = Button(self.editor, bg=bg, fg=fc, font=font,
                                    text='OPEN FILE', command=lambda: self.open_file(use_path=True))
        self.file_list = FileList(
            self, editor=self.editor, button=self.open_file_btn, bg=bg, oc=oc, font=font)
        self.num_line = NumLine(self, editor=self.editor, bg=bg, fg=fg, font=font)

        def yview(*args):
            self.editor.yview(*args)
            self.num_line.yview(*args)
        self.scrolly.config(command=yview)

        def set(*args, nl=True):
            if not nl:
                yview('moveto', args[0])
            self.scrolly.set(*args)
        self.num_line.config(yscrollcommand=set)
        self.editor.config(yscrollcommand=lambda *args: set(*args, nl=False))

        self.file_manager.pack(fill='y', side='left')
        self.file_list.pack(fill='x', side='top')
        self.scrolly.pack(fill='y', side='left')
        self.editor.pack(fill='both', side='right', expand=1)
        self.num_line.pack(fill='y', side='right')
        self.open_file_btn.pack()

        if path == '':
            return

        if isfile(path):
            self.open_file(path)
        elif isdir(path):
            self.open_folder(path)
        else:
            if '.' in basename(path):
                system(f'touch {abspath(path)}')
                self.open_file(path)
            else:
                system(f'mkdir {abspath(path)}')
                self.open_folder(path)

    def open_file(self, path='', use_path=False):
        file = askopenfilename() if path == '' else path
        if file in [(), '']:
            return
        self.open_file_btn.forget()
        self.editor.open(file)
        if file in list(self.file_list.opened):
            return
        self.file_list.open(path=path)

    def open_folder(self, path=''):
        folder = askdirectory() if path == '' else path
        if folder in [(), '']:
            return
        self.open_file_btn.forget()
        self.open_folder_btn.forget()
        self.file_manager.open(folder)

    def close_file(self, file):
        self.file_list.close(file)

    def close_folder(self):
        self.file_manager.open()
        for file in list(self.file_list.opened):
            self.close_file(file=file)
        self.open_folder_btn.pack()
        self.open_file_btn.pack()

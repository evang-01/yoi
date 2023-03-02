from tkinter import *
from tkinter.filedialog import *
from tkinter.font import Font
from yoi.editor import *
from yoi.file_manager import *
from os.path import basename, isfile


class Yoi(Frame):
    def __init__(self, root, path='', bg='#000', fg='#fff', dc='#f0f', fc='#0f0', fw=32,
                 oc='#0ff', sg='#00f', font=('Courier', 12, 'bold'), indent=16, tabs=4):
        super().__init__(root)
        self.bg = bg
        self.oc = oc
        self.font = font
        self.config(bg=bg)

        self.file_manager = FileManager(self, bg=bg, oc=oc, font=font,
                                        width=fw,
                                        fc=fc, dc=dc, indent=indent)
        self.open_folder_btn = Button(self.file_manager, bg=bg, fg=dc,
                                      font=font, text='OPEN FOLDER',
                                      command=lambda: self.open_folder())
        self.open_folder_btn.pack()
        self.file_manager.pack(fill='y', side='left')

        self.opened = dict()
        self.files = Frame(self, bg=bg)
        self.files.pack(fill='x', side='top')

        self.scrolly = Scrollbar(self)
        self.editor = Editor(self, path='', bg=bg, insertbackground=fg,
                             tabs=Font(font=font).measure(' '*tabs),
                             selectbackground=sg, fg=fg, font=font,
                             yscrollcommand=self.scrolly.set)
        self.open_file_btn = Button(self.editor, bg=bg, fg=fc,
                                    font=font, text='OPEN FILE',
                                    command=lambda: self.open_file(use_path=True))
        self.open_file_btn.pack()
        self.editor.pack(fill='both', side='right', expand=1)
        self.scrolly.pack(fill='y', side='right')

        if isfile(path) and path != '':
            self.open_file(path=path)
        elif path != '':
            self.open_folder(path=path)

    def open_file(self, path='', use_path=False):
        file = askopenfilename() if path == '' else path
        if file in [(), '']:
            return
        self.open_file_btn.forget()
        self.editor.open(file)
        if file in self.opened:
            return
        f = Frame(self.files)
        Button(f, text=file if use_path else basename(file),
               bg=self.bg, fg=self.oc, font=self.font,
               command=lambda f=file: self.editor.open(f)).pack(side='left')
        Button(f, text='x', bg=self.bg, fg='#f00', font=self.font,
               command=lambda f=file: self.close_file(f)).pack(side='right')
        f.pack(side='right')
        self.opened[file] = f

    def open_folder(self, path=''):
        folder = askdirectory() if path == '' else path
        if folder in [(), '']:
            return
        self.open_file_btn.forget()
        self.open_folder_btn.forget()
        self.file_manager.open(folder, lambda file: self.open_file(file))

    def close_file(self, file):
        self.opened[file].destroy()
        del self.opened[file]
        last = list(self.opened.keys())[-1]\
            if self.opened != {} else ''
        if self.opened == {}:
            self.open_file_btn.pack()
            self.editor.open('')
            self.editor['state'] = 'disabled'
        self.editor.open(last)

    def close_folder(self):
        self.file_manager.open()
        for file in self.opened.keys():
            self.close_file(file=file)
        self.open_folder_btn.pack()
        self.open_file_btn.pack()


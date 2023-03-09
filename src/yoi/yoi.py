from os.path import isfile
from tkinter import Frame, Scrollbar, Button
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.font import Font
from yoi.editor import Editor
from yoi.file_manager import FileManager
from yoi.file_list import FileList


class Yoi(Frame):
    def __init__(self, root, path='', bg='#000', fg='#fff', dc='#f0f', fc='#0f0', tags={
            'builtin': '#0f0',
            'class': '#0f0',
            'function': '#0f0',
            'comment': '#00f',
            'keyword': '#f0f',
            'literal': '#ff0',
            'punctuation': '#f00',
            'operator': '#0ff'
    }, fw=32, oc='#0ff', sg='#00f', font=('Courier', 12, 'bold'), indent=16, tabs=4):
        super().__init__(root)
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
            self, orient='vertical', bg=oc, activebackground=fc, troughcolor=bg)
        self.editor = Editor(self, path='', tags=tags, bg=bg, insertbackground=fg, tabs=Font(font=font).measure(
            ' ' * tabs), selectbackground=sg, selectforeground=fg, inactiveselectbackground=sg, fg=fg, font=font, yscrollcommand=self.scrolly.set)
        self.open_file_btn = Button(self.editor, bg=bg, fg=fc, font=font,
                                    text='OPEN FILE', command=lambda: self.open_file(use_path=True))
        self.file_list = FileList(
            self, editor=self.editor, button=self.open_file_btn, bg=bg, oc=oc, font=font)
        self.scrolly.config(command=self.editor.yview)

        self.file_manager.pack(fill='y', side='left')
        self.file_list.pack(fill='x', side='top')
        self.editor.pack(fill='both', side='right', expand=1)
        self.scrolly.pack(fill='y', side='right')
        self.open_file_btn.pack()

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

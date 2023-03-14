from yoi import Editor

@Editor.bind_change
def main(self):
    print(self.get_cursor(True))

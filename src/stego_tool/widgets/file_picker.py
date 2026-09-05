from textual.screen import Screen
from textual.widgets import DirectoryTree
from textual.message import Message

class FileSelected(Message):
    def __init__(self, path):
        super().__init__()
        self.path = path

class FilePicker(Screen):
    def compose(self):
        yield DirectoryTree(".", id="directory_tree")

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        self.post_message(FileSelected(event.path))
        self.dismiss(FileSelected(event.path))


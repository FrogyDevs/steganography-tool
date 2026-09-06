from textual.screen import Screen
from textual.widgets import  Static, OptionList
from textual.widgets.option_list import Option
from stego_tool.screens.encode import EncodeScreen
from stego_tool.screens.decode import DecodeScreen
from stego_tool.screens.clear import ClearScreen

class HomeScreen(Screen):
    def compose(self):
        yield Static("Welcome to the Stego Tool!")
        yield OptionList(
            Option("Encode", id="encode"),
            Option("Decode", id="decode"),
            Option("Clear", id="clear"),
            Option('Quit', id='quit')
        )

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option.id == "encode":
            self.app.push_screen(EncodeScreen())
        elif event.option.id == "decode":
            self.app.push_screen(DecodeScreen())
        elif event.option.id == "clear":
            self.app.push_screen(ClearScreen())
        elif event.option.id == 'quit':
            self.app.exit()

    def on_mount(self) -> None:
        self.screen.styles.background = "#1a1b26"
from textual.screen import Screen
from textual.widgets import  Static, OptionList
from textual.widgets.option_list import Option
from stego_tool.screens.encode import EncodeScreen

class HomeScreen(Screen):
    def compose(self):
        yield Static("Welcome to the Stego Tool!")
        yield OptionList(
            Option("Encode", id="encode"),
            Option("Decode", id="decode"),
            Option("Settings", id="settings"),
        )

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option.id == "encode":
            self.app.push_screen(EncodeScreen())
        elif event.option.id == "decode":
            # Handle decode option
            pass
        elif event.option.id == "settings":
            # Handle settings option
            pass

    def on_mount(self) -> None:
        self.screen.styles.background = "#1a1b26"
from textual.app import App
from stego_tool.screens.home import HomeScreen

class StegoApp(App):
    def on_mount(self) -> None:
        self.push_screen(HomeScreen())
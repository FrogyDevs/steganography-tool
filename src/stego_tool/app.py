from textual.app import App

class StegoApp(App):
    def on_mount(self) -> None:
        self.push_screen("home")
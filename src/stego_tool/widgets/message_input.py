from textual.screen import Screen
from textual.widgets import Label, Input
from textual.message import Message


class MessageSubmitted(Message):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


class MessageInput(Screen):
    def compose(self):
        yield Label("Enter the secret message to hide:")
        yield Input(placeholder="Secret message", id="message-input")

    def on_mount(self) -> None:
        self.query_one(Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(MessageSubmitted(event.value))

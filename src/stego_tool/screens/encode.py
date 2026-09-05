from textual.screen import Screen
from textual.widgets import Label, Static
from pathlib import Path

from stego_tool.widgets.file_picker import FilePicker, FileSelected
from stego_tool.widgets.message_input import MessageInput, MessageSubmitted

from stego_tool.codecs.text import TextCodec
from stego_tool.codecs.image import ImageCodec
from stego_tool.codecs.pdf import PdfCodec
from stego_tool.codecs.audio import AudioCodec
from stego_tool.codecs.video import VideoCodec

CODEC_MAPPING = {
    '.txt': TextCodec,
    '.png': ImageCodec,
    '.jpg': ImageCodec,
    '.jpeg': ImageCodec,
    '.pdf': PdfCodec,
    '.mp3': AudioCodec,
    '.wav': AudioCodec,
    '.mp4': VideoCodec,
    '.avi': VideoCodec,
    '.mkv': VideoCodec,
}

class EncodeScreen(Screen):
    def compose(self):
        yield Static("Encode Screen")
        yield Label("Selected file: ", id="result-label")

    def on_mount(self) -> None:
        self.styles.background = "#1a1b26"
        self._codec_cls = None
        self._selected_path: Path | None = None
        self.app.push_screen(FilePicker(), callback=self.on_file_selected)

    def on_file_selected(self, selected: FileSelected | None) -> None:
        if selected is None:
            return

        path = Path(selected.path)
        codec_cls = CODEC_MAPPING.get(path.suffix.lower())
        if codec_cls is None:
            self.query_one('#result-label', Label).update(f"Unsupported file type: {path.suffix}")
            return

        self._selected_path = path
        self._codec_cls = codec_cls
        self.query_one('#result-label', Label).update(f"Selected file: {path}")
        self.app.push_screen(MessageInput(), callback=self.on_message_entered)

    def on_message_entered(self, submitted: MessageSubmitted | None) -> None:
        label = self.query_one('#result-label', Label)
        if submitted is None or not submitted.message:
            label.update("Encoding cancelled: no message entered.")
            return

        codec = self._codec_cls(str(self._selected_path), submitted.message)
        try:
            result = codec.encode()
        except Exception as exc:
            label.update(f"Encoding failed: {exc}")
            return

        label.update(f"Encoded successfully: {result}")
        self.set_timer(3, self.app.pop_screen())  # Automatically pop the screen after 3 seconds

from textual.screen import Screen
from textual.widgets import Label, Static
from pathlib import Path

from stego_tool.widgets.file_picker import FilePicker, FileSelected

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


class ClearScreen(Screen):
    def compose(self):
        yield Static("Clear Screen")
        yield Label("Selected file: ", id="result-label")
        yield Label('', id='feedback')

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
        codec = self._codec_cls(str(self._selected_path))
        try:
            result = codec.clear()
            self.query_one('#feedback', Label).update(result)
        except Exception as exc:
            self.query_one('#feedback', Label).update(f'ERROR: {exc}')
            return

        self.app.set_timer(3, self.app.pop_screen)

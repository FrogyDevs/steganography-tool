from pathlib import Path

from pypdf import PdfWriter, PdfReader


class PdfCodec:
    def __init__(self, carrier, secret=None):
        self.carrier = carrier
        self.secret = secret

    def _write_in_place(self, target_path, writer):
        target = Path(target_path)
        temp_path = target.with_name(f"{target.stem}.tmp{target.suffix}")
        writer(temp_path)
        if temp_path.exists():
            temp_path.replace(target)

    def encode(self):
        def writer(temp_path: Path):
            writer_obj = PdfWriter()
            writer_obj.append(PdfReader(self.carrier))
            writer_obj.add_metadata({"/HiddenMessage": self.secret})
            writer_obj.write(str(temp_path))

        self._write_in_place(self.carrier, writer)
        return "Encoded"

    def decode(self):
        reader = PdfReader(self.carrier)
        metadata = reader.metadata
        return metadata.get("/HiddenMessage", "No hidden message found")
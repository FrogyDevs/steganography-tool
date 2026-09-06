from pathlib import Path


class AudioCodec:
    def __init__(self, carrier, secret=None):
        if not carrier.endswith('.mp3'):
            raise ValueError("Carrier must be an MP3 file.")
        self.carrier = carrier
        self.secret = secret
        self.start_marker = b'%%HIDDEN_START%%'
        self.end_marker = b'%%HIDDEN_END%%'

    def _write_in_place(self, target_path, writer):
        target = Path(target_path)
        temp_path = target.with_name(f"{target.stem}.tmp{target.suffix}")
        writer(temp_path)
        if temp_path.exists():
            temp_path.replace(target)

    def encode(self):
        if self.secret is None:
            raise ValueError("Secret message is required for encoding.")

        def writer(temp_path: Path):
            with open(self.carrier, 'rb') as f:
                content = f.read()

            payload = self.start_marker + self.secret.encode('utf-8') + self.end_marker
            temp_path.write_bytes(content + payload)

        self._write_in_place(self.carrier, writer)
        return "Message hidden in audio file successfully."

    def decode(self):
        with open(self.carrier, 'rb') as f:
            content = f.read()

        start = content.find(self.start_marker)
        end = content.find(self.end_marker)

        if start == -1 or end == -1:
            return "No hidden message found."

        start += len(self.start_marker)
        return content[start:end].decode('utf-8', errors='replace')

    def clear(self):
        with open(self.carrier, 'rb') as f:
            content = f.read()

        start = content.find(self.start_marker)
        end = content.find(self.end_marker)

        if start == -1 or end == -1:
            return "No hidden message found; file unchanged."

        def writer(temp_path: Path):
            temp_path.write_bytes(content[:start])

        self._write_in_place(self.carrier, writer)
        return "Cleared"

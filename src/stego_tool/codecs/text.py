from pathlib import Path


class TextCodec:
    def __init__(self, carrier="", secret=None):
        self.carrier = str(carrier)
        self.secret = secret

    def _write_in_place(self, target_path, writer):
        target = Path(target_path)
        temp_path = target.with_name(f"{target.stem}.tmp{target.suffix}")
        writer(temp_path)
        if temp_path.exists():
            temp_path.replace(target)

    def _read_file(self, path=None):
        path = Path(path or self.carrier)
        with path.open(encoding='utf-8') as f:
            return f.read()

    def encode(self, input_path=None, output_path=None, message=None):
        input_path = str(input_path or self.carrier)
        output_path = str(output_path or input_path)
        message = message if message is not None else self.secret
        if message is None:
            raise ValueError('Secret message is required for encoding.')

        def writer(temp_path: Path):
            bits = ''.join(format(ord(c), '08b') for c in message)
            hidden = ''.join('\u200b' if b == '0' else '\u200c' for b in bits)
            carrier_content = Path(input_path).read_text(encoding='utf-8')
            encoded_content = carrier_content[:4] + hidden + carrier_content[4:]
            temp_path.write_text(encoded_content, encoding='utf-8')

        self._write_in_place(output_path, writer)
        return Path(output_path).read_text(encoding='utf-8')

    def decode(self, input_path=None):
        input_path = str(input_path or self.carrier)
        stego_text = Path(input_path).read_text(encoding='utf-8')
        if stego_text is None:
            raise ValueError('stego_text is required for decoding')

        bits = ''.join(
            '0' if character == '\u200b' else '1'
            for character in stego_text
            if character in '\u200b\u200c'
        )
        if not bits:
            return ''

        chars = [
            chr(int(bits[index:index + 8], 2))
            for index in range(0, len(bits) - 7, 8)
        ]
        return ''.join(chars)

    def clear(self, input_path=None, output_path=None):
        input_path = str(input_path or self.carrier)
        output_path = str(output_path or input_path)

        carrier_content = Path(input_path).read_text(encoding='utf-8')
        if not any(character in '​‌' for character in carrier_content):
            return 'No hidden message found; file unchanged.'

        def writer(temp_path: Path):
            cleaned_content = ''.join(
                character for character in carrier_content if character not in '​‌'
            )
            temp_path.write_text(cleaned_content, encoding='utf-8')

        self._write_in_place(output_path, writer)
        return 'Cleared'

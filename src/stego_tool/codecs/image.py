from pathlib import Path

from PIL import Image


class ImageCodec:
    DELIMITER = '1111111111111110'

    def __init__(self, carrier="", secret=None):
        self.carrier = str(carrier)
        self.secret = secret
        self.type = Path(self.carrier).suffix.lower() if self.carrier else '.png'

    def _write_in_place(self, target_path, writer):
        target = Path(target_path)
        temp_path = target.with_name(f"{target.stem}.tmp{target.suffix}")
        writer(temp_path)
        if temp_path.exists():
            temp_path.replace(target)

    def _text_to_bits(self, txt: str):
        return ''.join(format(byte, '08b') for byte in txt.encode('utf-8'))

    def _bits_to_text(self, bits: str):
        byte_chunks = [bits[i:i + 8] for i in range(0, len(bits), 8)]
        byte_values = [int(b, 2) for b in byte_chunks]
        return bytes(byte_values).decode('utf-8', errors='replace')

    def encode(self, input_path: str | None = None, output_path: str | None = None, msg: str | None = None):
        input_path = str(input_path or self.carrier)
        output_path = str(output_path or input_path)
        msg = msg if msg is not None else self.secret
        if msg is None:
            raise ValueError('Secret message is required for encoding.')

        def writer(temp_path: Path):
            img = Image.open(input_path).convert('RGB')
            pixels = list(img.getdata())

            bits = self._text_to_bits(msg) + self.DELIMITER
            capacity = len(pixels) * 3
            if len(bits) > capacity:
                raise ValueError('Message too large')
            bit_iter = iter(bits)
            new_pixels = []

            for r, g, b in pixels:
                channels = [r, g, b]
                for i in range(3):
                    bit = next(bit_iter, None)
                    if bit is not None:
                        channels[i] = (channels[i] & ~1) | int(bit)
                new_pixels.append(tuple(channels))

            out = Image.new('RGB', img.size)
            out.putdata(new_pixels)
            out.save(temp_path)

        self._write_in_place(output_path, writer)
        return 'Saved'

    def decode(self, carrier_file: str | None = None):
        carrier_file = carrier_file or self.carrier
        img = Image.open(carrier_file).convert('RGB')
        pixels = img.getdata()

        bits = []
        for r, g, b in pixels:
            for channel in (r, g, b):
                bits.append(str(channel & 1))
                if len(bits) >= 16 and ''.join(bits[-16:]) == self.DELIMITER:
                    message_bits = ''.join(bits[:-16])
                    return self._bits_to_text(message_bits)
        raise ValueError('delimiter not present in the image - no hidden message found')
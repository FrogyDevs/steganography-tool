from PIL import Image

class ImageCodec:
    DELIMITER = '1111111111111110'

    def _read_file(self):
        with open(self.carrier, encoding='utf-8') as f:
            content = f.read()
            return content        

    def _text_to_bits(self, txt: str):
        return ''.join(format(byte, '08b') for byte in txt.encode('utf-8'))

    def _bits_to_text(self, bits: str):
        byte_chunks = [bits[i:i + 8] for i in range(0, len(bits), 8)]
        byte_values = [int(b, 2) for b in byte_chunks]
        return bytes(byte_values).decode('utf-8', errors='replace')

    def encode(self, input_path: str, output_path: str, msg: str):
        img = Image.open(input_path).convert('RGB')
        pixels = list(img.getdata())

        bits = self._text_to_bits(msg) + self.DELIMITER
        capacity = len(pixels) * 3
        if len(bits) > capacity:
            raise ValueError(f'Message too large')
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
        out.save(f'output/image{self.type}')
        return 'Saved'

    def decode(self, carrier_file: str):
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
import sys
from PIL import Image
from pypdf import PdfReader, PdfWriter
import cv2
import numpy as np

class text_based(): 
        def __init__(self, carrier, secret=None): #secret is the text to encode; carrier text of file
            self.carrier = carrier
            self.secret = secret

        def _read_file(self):
            with open(self.carrier, encoding='utf-8') as f:
                content = f.read()
                return content        
            
        def encode(self):
            bits = ''.join(format(ord(c), '08b') for c in self.secret)
            hidden = ''.join('\u200b' if b == '0' else '\u200c' for b in bits)
            carrier_content = self._read_file()
            encoded_content = carrier_content[:4] + hidden + carrier_content[4:]
            with open('output.txt', 'w', encoding='utf-8') as f:
                f.write(encoded_content)
            return encoded_content
        

        def decode(self):
             with open(self.carrier, encoding='utf-8') as f:
                  stego_text = f.read()
             if stego_text is None:
                 raise ValueError('stego_text is required for decoding')

             bits = ''.join(
                 '0' if character == '\u200b' else '1'
                 for character in stego_text
                 if character in '\u200b\u200c'
             )
             chars = [
                 chr(int(bits[index:index + 8], 2))
                 for index in range(0, len(bits) - 7, 8)
             ]
             return ''.join(chars)

class image_based():
    def __init__(self, carrier, secret=None): #secret is the text to encode; carrier text of file
        self.carrier = carrier
        self.secret = secret
        self.type = '.png' if carrier.endswith('.png') else '.bmp'
        self.delimeter = '1111111111111110'

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

    def encode(self, carrier_file: str, msg: str):
        img = Image.open(carrier_file).convert('RGB')
        pixels = list(img.getdata())

        bits = self._text_to_bits(msg) + self.delimeter
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
                if len(bits) >= 16 and ''.join(bits[-16:]) == self.delimeter:
                    message_bits = ''.join(bits[:-16])
                    return self._bits_to_text(message_bits)
        raise ValueError('delimiter not present in the image - no hidden message found')

class pdf_based:
    def __init__(self, carrier, secret=None):
        self.carrier = carrier
        self.secret = secret

    def encode(self):
        writer = PdfWriter()
        writer.append(PdfReader(self.carrier))
        writer.add_metadata({"/HiddenMessage": self.secret})
        writer.write("output/output.pdf")
        
    def decode(self):
        reader = PdfReader(self.carrier)
        metadata = reader.metadata
        return metadata.get("/HiddenMessage", "No hidden message found")

class audio_based:
    def __init__(self, carrier, secret=None):
        if not carrier.endswith('.mp3'):
            raise ValueError("Carrier must be an MP3 file.")
        self.carrier = carrier
        self.secret = secret
        self.start_marker = b'%%HIDDEN_START%%'
        self.end_marker = b'%%HIDDEN_END%%'

    def encode(self):
        if self.secret is None:
            raise ValueError("Secret message is required for encoding.")

        with open(self.carrier, 'rb') as f:
            content = f.read()

        payload = self.start_marker + self.secret.encode('utf-8') + self.end_marker
        new_content = content + payload

        with open('output/output.mp3', 'wb') as f:
            f.write(new_content)

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

class video_based:
    def __init__(self, carrier, secret=None):
        self.carrier = carrier
        self.secret = secret
        self.delimiter = '1111111111111110'
        self.type = '.avi' if carrier.endswith('.avi') else '.mkv'

    def _text_to_bits(self, txt: str):
        return ''.join(format(byte, '08b') for byte in txt.encode('utf-8'))

    def _bits_to_text(self, bits: str):
        byte_chunks = [bits[i:i + 8] for i in range(0, len(bits), 8)]
        byte_values = [int(b, 2) for b in byte_chunks]
        return bytes(byte_values).decode('utf-8', errors='replace')

    def encode(self):
        output_file = f'output/output{self.type}'
        if self.secret is None:
            raise ValueError("Secret message is required for encoding.")

        cap = cv2.VideoCapture(self.carrier)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*'FFV1')
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

        bits = self._text_to_bits(self.secret) + self.delimiter
        bit_iter = iter(bits)
        done = False

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if not done:
                flat = frame.reshape(-1) # flatten the frame to 1D array
                for i in range(len(flat)):
                    bit = next(bit_iter, None)
                    if bit is None:
                        done = True
                        break
                    flat[i] = (flat[i] & np.uint8(0xFE)) | np.uint8(bit)
                frame = flat.reshape(frame.shape) # reshape back to original frame shape
            out.write(frame)

        cap.release()
        out.release()
        return "Message hidden in video file successfully."

    def decode(self):
        cap = cv2.VideoCapture(f'output/output{self.type}')
        bits = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            flat = frame.reshape(-1) # flatten the frame to 1D array
            for byte in flat:
                bits.append(str(byte & 1))
                if len(bits) >= 16 and ''.join(bits[-16:]) == self.delimiter:
                    message_bits = ''.join(bits[:-16])
                    cap.release()
                    return self._bits_to_text(message_bits)
        cap.release()
        return "No hidden message found."
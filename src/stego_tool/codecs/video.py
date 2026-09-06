from pathlib import Path

import cv2
import numpy as np


class VideoCodec:
    def __init__(self, carrier, secret=None):
        self.carrier = carrier
        self.secret = secret
        self.delimiter = '1111111111111110'
        self.type = '.avi' if carrier.endswith('.avi') else '.mkv'

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

    def encode(self):
        if self.secret is None:
            raise ValueError("Secret message is required for encoding.")

        def writer(temp_path: Path):
            cap = cv2.VideoCapture(self.carrier)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            fourcc = cv2.VideoWriter_fourcc(*'FFV1')
            out = cv2.VideoWriter(str(temp_path), fourcc, fps, (width, height))

            bits = self._text_to_bits(self.secret) + self.delimiter
            bit_iter = iter(bits)
            done = False

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                if not done:
                    flat = frame.reshape(-1)
                    for i in range(len(flat)):
                        bit = next(bit_iter, None)
                        if bit is None:
                            done = True
                            break
                        flat[i] = (flat[i] & np.uint8(0xFE)) | np.uint8(bit)
                    frame = flat.reshape(frame.shape)
                out.write(frame)

            cap.release()
            out.release()

        self._write_in_place(self.carrier, writer)
        return "Message hidden in video file successfully."

    def decode(self):
        cap = cv2.VideoCapture(self.carrier)
        bits = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            flat = frame.reshape(-1)
            for byte in flat:
                bits.append(str(byte & 1))
                if len(bits) >= 16 and ''.join(bits[-16:]) == self.delimiter:
                    message_bits = ''.join(bits[:-16])
                    cap.release()
                    return self._bits_to_text(message_bits)
        cap.release()
        return "No hidden message found."

    def _has_hidden_message(self) -> bool:
        cap = cv2.VideoCapture(self.carrier)
        bits = []
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                flat = frame.reshape(-1)
                for byte in flat:
                    bits.append(str(byte & 1))
                    if len(bits) >= 16 and ''.join(bits[-16:]) == self.delimiter:
                        return True
            return False
        finally:
            cap.release()

    def clear(self):
        if not self._has_hidden_message():
            return "No hidden message found; file unchanged."

        def writer(temp_path: Path):
            cap = cv2.VideoCapture(self.carrier)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            fourcc = cv2.VideoWriter_fourcc(*'FFV1')
            out = cv2.VideoWriter(str(temp_path), fourcc, fps, (width, height))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                flat = frame.reshape(-1)
                flat &= np.uint8(0xFE)
                frame = flat.reshape(frame.shape)
                out.write(frame)

            cap.release()
            out.release()

        self._write_in_place(self.carrier, writer)
        return "Cleared"

import cv2
import numpy as np

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

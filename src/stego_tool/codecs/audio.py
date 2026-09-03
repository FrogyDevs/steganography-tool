class AudioCodec:
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

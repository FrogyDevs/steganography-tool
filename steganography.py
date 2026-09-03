class text_based(): 
        def __init__(self, carrier, secret, stego_text=None): #secret is the text to encode; carrier text of file
            self.carrier = carrier
            self.secret = secret
            self.stego_text = stego_text

        
             

        def encode(self):
            bits = ''.join(format(ord(c), '08b') for c in self.secret)
            hidden = ''.join('\u200b' if b == '0' else '\u200c' for b in bits)
            return self.carrier[:4] + hidden + self.carrier[4:]

        def decode(self, stego_text=None):
             stego_text = stego_text or self.stego_text
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
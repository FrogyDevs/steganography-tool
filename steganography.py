import sys
from PIL import Image

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


    
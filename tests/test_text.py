from src.stego_tool.codecs.text import TextCodec

def text_encoder(inputfile: str, msg: str):
    encoder = TextCodec(inputfile, msg)
    encoded_content = encoder.encode()
    with open('test.txt', encoding='utf-8') as f:
        len_txt = f.read()
    print(f'Len of original text:\n {len(len_txt)}')
    print(f'Len of encoded text:\n{len(encoded_content)}')

def text_decoder(inputfile: str):
    decoder = TextCodec(inputfile)
    decoded_txt = decoder.decode()
    print(decoded_txt)
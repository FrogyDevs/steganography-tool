from steganography import text_based, image_based, pdf_based, audio_based, video_based

def op_selector():
    print(f'choose an operation (1-3):\n1)    hide\n2)    reveal\n3)  capacity')
    selected = input()
    return selected

def carrier_type():
    print(f'choose a carrier (1-5)\ntext')
    selected = input()
    return selected

def text_encoder(inputfile: str, msg: str):
    encoder = text_based(inputfile, msg)
    encoded_content = encoder.encode()
    with open('test.txt', encoding='utf-8') as f:
        len_txt = f.read()
    print(f'Len of original text:\n {len(len_txt)}')
    print(f'Len of encoded text:\n{len(encoded_content)}')

def text_decoder(inputfile: str):
    decoder = text_based(inputfile)
    decoded_txt = decoder.decode()
    print(decoded_txt)

def image_encoder(inputfile: str, msg: str):
    encoder = image_based(inputfile, msg)
    encoder.encode(inputfile, msg)

def image_decoder(inputfile: str):
    decoder = image_based(inputfile)
    decoded_msg = decoder.decode(inputfile)
    print(decoded_msg)

def pdf_encoder(inputfile: str, msg: str):
    encoder = pdf_based(inputfile, msg)
    encoder.encode()

def pdf_decoder(inputfile: str):
    decoder = pdf_based(inputfile)
    decoded_msg = decoder.decode()
    print(decoded_msg)

def audio_encoder(inputfile: str, msg: str):
    encoder = audio_based(inputfile, msg)
    encoder.encode()

def audio_decoder(inputfile: str):
    decoder = audio_based(inputfile)
    decoded_msg = decoder.decode()
    print(decoded_msg)

def video_encoder(inputfile: str, msg: str):
    encoder = video_based(inputfile, msg)
    encoder.encode()

def video_decoder(inputfile: str):
    decoder = video_based(inputfile)
    decoded_msg = decoder.decode()
    print(decoded_msg)

def main():
    video_encoder('input/input.mkv', 'This is a secret message hidden in the video file.')
    video_decoder('output/output.mkv')

if __name__ == "__main__":
    main()

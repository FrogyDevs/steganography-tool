from steganography import text_based

def op_selector():
    print(f'choose an operation (1-3):\n1)    hide\n2)    reveal\n3)  capacity')
    selected = input()
    return selected

def carrier_type():
    print(f'choose a carrier (1-5)\ntext')
    selected = input()
    return selected

def text_encrypt(inputfile: str, msg: str):
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

def main():
    text_decoder('output.txt')
    

if __name__ == "__main__":
    main()

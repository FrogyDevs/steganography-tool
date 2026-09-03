from steganography import text_based

def op_selector():
    print(f'choose an operation (1-3):\n1)    hide\n2)    reveal\n3)  capacity')
    selected = input()
    return selected

def carrier():
    print(f'choose a carrier (1-5)\ntext')
    selected = input()
def read_file(filepath):
    with open(filepath) as f:
        print(len(f.read()))
        return f.read()
            
def text_to_text_ecrypt():
    carrier = input(f'enter carrier filepath:\n')
    msg = input(f'enter message to hide:\n')
    textBased = text_based(carrier=read_file(carrier), secret=msg)
    print(textBased.encode())
    with open('testfile/output/text.txt') as f:
        f.write(textBased.encode())
        print(len(f.read()))
    return f'Encoded file {carrier}'

def main():
    text_to_text_ecrypt()


if __name__ == "__main__":
    main()

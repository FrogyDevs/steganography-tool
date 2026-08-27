from steganography import text_based

def op_selector():
    print(f'choose an operation (1-3):\n1)    hide\n2)    reveal\n3)  capacity')
    selected = input()
    return selected

def carrier():
    print(f'choose a carrier (1-5)\ntext')
    selected = input()



def main():
    selected_op = op_selector()
    selected_car = carrier()
    text = text_based("Meet me at the usual place.", "hello world")
    stego_text = text.encode()
    print(stego_text)
    print(text.decode(stego_text))

if __name__ == "__main__":
    main()

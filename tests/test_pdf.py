from src.stego_tool.codecs.pdf import PDFCodec


def pdf_encoder(inputfile: str, msg: str):
    encoder = PDFCodec(inputfile, msg)
    encoder.encode()

def pdf_decoder(inputfile: str):
    decoder = PDFCodec(inputfile)
    decoded_msg = decoder.decode()
    print(decoded_msg)
from stego_tool.codecs.image import ImageCodec

def image_encoder(inputfile: str, msg: str):
    encoder = ImageCodec(inputfile, msg)
    encoder.encode()

def image_decoder(inputfile: str):
    decoder = ImageCodec(inputfile)
    decoded_msg = decoder.decode(inputfile)
    print(decoded_msg)
from stego_tool.codecs.audio import AudioCodec


def audio_encoder(inputfile: str, msg: str):
    encoder = AudioCodec(inputfile, msg)
    encoder.encode()

def audio_decoder(inputfile: str):
    decoder = AudioCodec(inputfile)
    decoded_msg = decoder.decode()
    print(decoded_msg)
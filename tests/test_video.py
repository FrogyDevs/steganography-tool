from src.stego_tool.codecs.video import VideoCodec


def video_encoder(inputfile: str, msg: str):
    encoder = VideoCodec(inputfile, msg)
    encoder.encode()

def video_decoder(inputfile: str):
    decoder = VideoCodec(inputfile)
    decoded_msg = decoder.decode()
    print(decoded_msg)
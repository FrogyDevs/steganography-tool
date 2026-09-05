from pathlib import Path

from PIL import Image

from stego_tool.codecs.image import ImageCodec
from stego_tool.codecs.text import TextCodec


def test_image_encode_overwrites_input_path(tmp_path):
    image_path = tmp_path / "carrier.png"
    Image.new("RGB", (10, 10), "white").save(image_path)
    original = image_path.read_bytes()

    codec = ImageCodec(str(image_path), "secret")
    codec.encode()

    assert image_path.exists()
    assert image_path.read_bytes() != original


def test_text_encode_overwrites_input_path(tmp_path):
    text_path = tmp_path / "carrier.txt"
    text_path.write_text("hello world", encoding="utf-8")

    codec = TextCodec(str(text_path), "secret")
    codec.encode()

    assert text_path.exists()
    assert text_path.read_text(encoding="utf-8") != "hello world"

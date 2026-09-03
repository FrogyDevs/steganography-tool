from pypdf import PdfWriter, PdfReader


class PdfCodec:
    def __init__(self, carrier, secret=None):
        self.carrier = carrier
        self.secret = secret

    def encode(self):
        writer = PdfWriter()
        writer.append(PdfReader(self.carrier))
        writer.add_metadata({"/HiddenMessage": self.secret})
        writer.write("output/output.pdf")
        
    def decode(self):
        reader = PdfReader(self.carrier)
        metadata = reader.metadata
        return metadata.get("/HiddenMessage", "No hidden message found")
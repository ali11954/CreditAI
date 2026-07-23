from io import BytesIO
import qrcode
from PIL import Image
import barcode
from barcode.writer import ImageWriter


def generate_qr_code(data: str, size: int = 10) -> BytesIO:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output


def generate_barcode(data: str, barcode_type: str = "code128") -> BytesIO:
    if barcode_type == "code128":
        code_class = barcode.get_barclass('code128')
    elif barcode_type == "code39":
        code_class = barcode.get_barclass('code39')
    elif barcode_type == "ean13":
        code_class = barcode.get_barclass('ean13')
    else:
        code_class = barcode.get_barclass('code128')
    
    code = code_class(data, writer=ImageWriter())
    
    output = BytesIO()
    code.write(output)
    output.seek(0)
    return output


def generate_invoice_barcode(invoice_number: str) -> BytesIO:
    return generate_barcode(invoice_number, "code128")

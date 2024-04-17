import base64
import io

import pyzbar.pyzbar as pyzbar
import qrcode
from PIL import Image


def show_qrcode(base64_data):
    binary_data = base64.b64decode(base64_data)
    stream = io.BytesIO(binary_data)
    img = Image.open(stream)
    barcodes = pyzbar.decode(img)
    # 5.获取并打印二维码解析结果
    qrcode_url = barcodes[0].data.decode("utf-8")
    qr = qrcode.QRCode()
    qr.add_data(qrcode_url)
    qr.make(fit=True)
    # 在控制台以 ASCII 形式打印二维码
    qr.print_ascii(invert=True)

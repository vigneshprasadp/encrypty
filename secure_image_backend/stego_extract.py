from PIL import Image
import io


def extract_message(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    img = img.convert("RGB")

    data = list(img.getdata())
    binary = ""

    for pixel in data:
        r, g, b = pixel
        binary += str(r & 1)
        binary += str(g & 1)
        binary += str(b & 1)

        if "1111111111111110" in binary:
            break

    binary = binary.split("1111111111111110")[0]

    msg = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        msg += chr(int(byte, 2))

    return msg

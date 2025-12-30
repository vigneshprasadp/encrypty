from PIL import Image
import io


def hide_message_in_image(image_bytes, message):
    img = Image.open(io.BytesIO(image_bytes))
    img = img.convert("RGB")

    binary_msg = ''.join(format(ord(i), '08b') for i in message) + "1111111111111110"

    data = list(img.getdata())
    new_data = []

    msg_index = 0

    for pixel in data:
        r, g, b = pixel

        if msg_index < len(binary_msg):
            r = (r & ~1) | int(binary_msg[msg_index])
            msg_index += 1

        if msg_index < len(binary_msg):
            g = (g & ~1) | int(binary_msg[msg_index])
            msg_index += 1

        if msg_index < len(binary_msg):
            b = (b & ~1) | int(binary_msg[msg_index])
            msg_index += 1

        new_data.append((r, g, b))

    img.putdata(new_data)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

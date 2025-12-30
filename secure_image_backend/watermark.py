from PIL import Image, ImageDraw, ImageFont
import io

def add_watermark(image_bytes, text):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    watermark = Image.new("RGBA", img.size)
    draw = ImageDraw.Draw(watermark)

    font_size = int(min(img.size) / 12)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    width, height = img.size
    draw.text((width - width//3, height - height//6), text,
              fill=(255, 255, 255, 180), font=font)

    combined = Image.alpha_composite(img, watermark)
    buffer = io.BytesIO()
    combined.convert("RGB").save(buffer, format="PNG")
    return buffer.getvalue()

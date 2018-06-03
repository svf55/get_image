import sys
from PIL import Image, ImageDraw


def gen_image_from_file(file_name, max_width=None, max_height=None):
    image = Image.open(file_name)

    if max_width or max_height:
        width = max_width or sys.maxsize
        height = max_height or sys.maxsize
        maxsize = (width, height)
        image.thumbnail(maxsize, Image.ANTIALIAS)

    return image


def gen_image_pil(width=150, height=150):

    image = Image.new("RGB", (width, height),
                      (131, 216, 237, 0))
    draw = ImageDraw.Draw(image)
    elipse_width = int(0.85 * width)
    elipse_height = int(0.85 * height)
    draw.ellipse(((width // 2 - elipse_width // 2),
                  (height // 2 - elipse_height // 2),
                  (width // 2 + elipse_width // 2),
                  (height // 2 + elipse_height // 2)),
                 fill="white", outline="blue")
    del draw

    return image


import sys
from PIL import Image, ImageDraw


def gen_image_from_file(file_name, image_max_width=None, image_max_height=None):
    image = Image.open(file_name)

    if image_max_width or image_max_height:
        width = image_max_width or sys.maxsize
        height = image_max_height or sys.maxsize
        maxsize = (width, height)
        image.thumbnail(maxsize, Image.ANTIALIAS)

    return image


def gen_image_pil(image_max_width=150, image_max_height=150):

    image = Image.new("RGB", (image_max_width, image_max_height),
                      (131, 216, 237, 0))
    draw = ImageDraw.Draw(image)
    elipse_width = int(0.85 * image_max_width)
    elipse_height = int(0.85 * image_max_height)
    draw.ellipse(((image_max_width // 2 - elipse_width // 2),
                  (image_max_height // 2 - elipse_height // 2),
                  (image_max_width // 2 + elipse_width // 2),
                  (image_max_height // 2 + elipse_height // 2)),
                 fill="white", outline="blue")
    del draw

    return image


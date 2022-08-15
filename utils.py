from PIL import Image
import numpy as np


def load_image(imagepath):
    image = Image.open(imagepath)
    img_data = np.array(list(image.getdata()), np.uint8)

    width, height = image.size
    return img_data, width, height


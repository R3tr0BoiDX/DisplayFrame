from PIL import Image

IMAGE_FILE_EXTENSION = ".png"


def get_image(_name):
    image = Image.open(str(_name) + IMAGE_FILE_EXTENSION)
    return image.load()


class Graphics:

    def __init__(self):
        pass

from PIL import Image

RESOURCES = "res"
DIGITS = "digits"
MISC = "misc"
WEATHER = "weather"
DAY = "day"
NIGHT = "night"

IMAGE_FILE_EXTENSION = ".png"


def digit(dig):
    return f"./{RESOURCES}/{DIGITS}/{str(dig)}{IMAGE_FILE_EXTENSION}"


def day(code):
    return f"./{RESOURCES}/{WEATHER}/{DAY}/{code}{IMAGE_FILE_EXTENSION}"


def night(code):
    return f"./{RESOURCES}/{WEATHER}/{NIGHT}/{code}{IMAGE_FILE_EXTENSION}"


def misc(name):
    return f"./{RESOURCES}/{MISC}/{name}{IMAGE_FILE_EXTENSION}"


class Graphics:

    def __init__(self):
        pass

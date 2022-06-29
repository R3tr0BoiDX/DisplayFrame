from PIL import Image

RESOURCES = "res"
DIGITS = "digits"
MISC = "misc"
WEATHER = "weather"
DAY = "day"
NIGHT = "night"

IMAGE_FILE_EXTENSION = ".png"

IMAGE_HEIGHT = 8
DIGIT_IMAGE_WIDTH = 4
WEATHER_IMAGE_WIDTH = 6


def digit(dig):
    return f"./{RESOURCES}/{DIGITS}/{str(dig)}{IMAGE_FILE_EXTENSION}"


def weather(code):
    if code[2] == 'd':
        return day(code)
    else:
        return night(code)


def day(code):
    return f"./{RESOURCES}/{WEATHER}/{DAY}/{code}{IMAGE_FILE_EXTENSION}"


def night(code):
    return f"./{RESOURCES}/{WEATHER}/{NIGHT}/{code}{IMAGE_FILE_EXTENSION}"


def misc(name):
    return f"./{RESOURCES}/{MISC}/{name}{IMAGE_FILE_EXTENSION}"

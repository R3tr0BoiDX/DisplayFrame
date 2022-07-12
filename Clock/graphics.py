# ./aseprite -b ./DisplayFrame.aseprite --save-as ./res/{slice}.png

RESOURCES = "res"
IMAGE_FILE_EXTENSION = ".png"

IMAGE_HEIGHT = 8
DIGIT_IMAGE_WIDTH = 4
WEATHER_IMAGE_WIDTH = 6


def get_filepath(filename):
    return f"./{RESOURCES}/{filename}{IMAGE_FILE_EXTENSION}"

import platform
import threading
import signal
import sys

from datetime import datetime
from rpi_ws281x import Color
from PIL import Image

import matrix
import graphics
import weather

UPDATE_WEATHER_CODE_INTERVAL = 120  # in seconds

X_OFFSET_START = 2
Y_OFFSET_START = 0

def get_current_time():
    now = datetime.now()
    return now.strftime("%H%M")


def display_resource(leds, image, x_offset=0, y_offset=0, render=True):
    pixel = image.convert("RGB")
    for x in range(image.width):
        for y in range(image.height):
            r, g, b = pixel.getpixel((x, y))
            matrix.setPixel(
                x + x_offset + X_OFFSET_START,
                y + y_offset + Y_OFFSET_START,
                Color(r, g, b),
                leds
            )

    if render:
        leds.show()


def display_digit(leds, digit, x_offset=0, y_offset=0, render=True):
    image = Image.open(graphics.get_filepath(str(digit)))
    display_resource(leds, image, x_offset, y_offset, render=render)


def display_weather(leds, code, x_offset=0, y_offset=0, render=True):
    image = Image.open(graphics.get_filepath(code))
    display_resource(leds, image, x_offset, y_offset, render=render)


def display_misc(leds, name, x_offset=0, y_offset=0, render=True):
    image = Image.open(graphics.get_filepath(name))
    display_resource(leds, image, x_offset, y_offset, render=render)


def display_time(leds, time, colon, render=True):
    matrix.flush(leds)

    colon_offset = 0
    for i in range(len(time)):
        if i == 2:
            if colon:
                display_misc(
                    leds,
                    "colon",
                    x_offset=(i * graphics.DIGIT_IMAGE_WIDTH) + 1,
                    render=False
                )
            colon_offset = 2

        display_digit(
            leds,
            time[i],
            x_offset=(i * graphics.DIGIT_IMAGE_WIDTH) + colon_offset,
            render=False
        )

    if render:
        leds.show()


class Main:

    def show_time(self):
        display_time(self.matrix.leds, get_current_time(), self.colon, render=False)
        self.colon = not self.colon

    def show_weather(self):
        display_weather(self.matrix.leds, self.weatherCode, x_offset=20, render=False)

    def show_all(self):
        threading.Timer(1, self.show_all).start()
        self.show_time()
        self.show_weather()
        self.matrix.leds.show()

    def update_weather_code(self):
        threading.Timer(UPDATE_WEATHER_CODE_INTERVAL, self.update_weather_code).start()
        self.weatherCode = weather.get_weather_code()

    def signal_handler(self, sig, frame):
        self.matrix.finish()
        sys.exit(0)

    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)

        self.colon = False
        self.weatherCode = weather.get_weather_code()

        if platform.processor() != "x86_64":
            self.matrix = matrix.Matrix()
            self.show_all()
            self.update_weather_code()


if __name__ == '__main__':
    Main()

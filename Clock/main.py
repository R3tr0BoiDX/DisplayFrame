import threading
import signal
import sys
import time

from rpi_ws281x import Color
from PIL import Image

import matrix
import graphics
import weather

UPDATE_WEATHER_CODE_INTERVAL = 120  # in seconds

X_OFFSET_START = 2
Y_OFFSET_START = 0
X_OFFSET_WEATHER = 21

DAY_BRIGHTNESS = 16
NIGHT_BRIGHTNESS = 2


def get_current_time():
    now = time.localtime()
    return time.strftime("%H%M", now)


def get_current_brightness(_sun):
    now = int(time.time())

    if _sun[0] < now < _sun[1]:
        print("It's night!")
        return DAY_BRIGHTNESS
    else:
        print("It's day!")
        return NIGHT_BRIGHTNESS


def display_resource(leds, image, x_offset=0, y_offset=0, render=True):
    pixel = image.convert("RGB")
    for x in range(image.width):
        for y in range(image.height):
            r, g, b = pixel.getpixel((x, y))
            matrix.set_pixel(
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
        display_weather(self.matrix.leds, self.weatherCode, x_offset=X_OFFSET_WEATHER, render=False)

    def set_current_brightness(self):
        matrix.set_brightness(get_current_brightness(self.sun), self.matrix.leds)

    def show_all(self):
        threading.Timer(1, self.show_all).start()
        self.show_time()
        self.show_weather()
        self.set_current_brightness()
        self.matrix.leds.show()

    def update_weather_and_sun(self):
        threading.Timer(UPDATE_WEATHER_CODE_INTERVAL, self.update_weather_and_sun).start()
        weather_and_sun = weather.get_weather_and_sun()
        self.weatherCode = weather_and_sun[0]
        self.sun = weather_and_sun[1]

    def signal_handler(self, sig, frame):
        self.matrix.finish()
        sys.exit(0)

    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)

        self.colon = False
        weather_and_sun = weather.get_weather_and_sun()
        self.weatherCode = weather_and_sun[0]
        self.sun = weather_and_sun[1]

        self.matrix = matrix.Matrix()
        self.show_all()
        self.update_weather_and_sun()


if __name__ == '__main__':
    Main()

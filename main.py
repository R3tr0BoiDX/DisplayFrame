import platform
import threading
import json
import signal
import sys

from datetime import datetime
from rpi_ws281x import Color
from PIL import Image

import matrix
import graphics
import weather


def get_current_time():
    now = datetime.now()
    return now.strftime("%H%M")


def read_config():
    with open('config.json') as f:
        return json.load(f)


def help_config():
    print("You need to config the config.json. You can use the config.example.json as starting point")
    print("See https://openweathermap.org/current for valid config entries")


def display_resource(leds, image, x_offset=0, y_offset=0, render=True):
    pixel = image.convert("RGB")
    for x in range(image.width):
        for y in range(image.height):
            r, g, b = pixel.getpixel((x, y))
            matrix.setPixel(
                x + x_offset,
                y + y_offset,
                Color(r, g, b),
                leds
            )

    if render:
        leds.show()


def display_digit(leds, digit, x_offset=0, y_offset=0, render=True):
    image = Image.open(graphics.digit(digit))
    display_resource(leds, image, x_offset, y_offset, render=render)


def display_weather_condition(leds, code, x_offset=0, y_offset=0, render=True):
    image = Image.open(graphics.weather(code))
    display_resource(leds, image, x_offset, y_offset, render=render)


def display_misc(leds, name, x_offset=0, y_offset=0, render=True):
    image = Image.open(graphics.misc(name))
    display_resource(leds, image, x_offset, y_offset, render=render)


def display_weather(leds):
    config = read_config()
    json_text = weather.request_weather(config)
    data = json.loads(json_text)
    code = weather.get_weather_icon_code(data)
    display_weather_condition(
        leds,
        code,
        x_offset=20
    )


def display_time(leds, time, colon):
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
    leds.show()


class Main:

    def show_time(self):
        threading.Timer(1, self.show_time).start()
        display_time(self.matrix.leds, get_current_time(), self.colon)
        self.colon = not self.colon

    def signal_handler(self, sig, frame):
        self.matrix.finish()
        sys.exit(0)

    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)

        self.colon = False

        if platform.processor() != "x86_64":
            self.matrix = matrix.Matrix()
            self.show_time()


if __name__ == '__main__':
    Main()

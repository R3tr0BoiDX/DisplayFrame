import platform

from PIL import Image

import matrix
import graphics

import requests
import json
import signal
import sys

from datetime import datetime
from rpi_ws281x import Color

URL = "https://api.openweathermap.org/data/2.5/weather"
TEST_URL = "https://httpbin.org/get"


def request_weather(_config):
    args = {
        'lat': _config["lat"],
        'lon': _config["lon"],
        "units": _config["units"],
        "mode": "json",  # must always be json
        "lang": _config["lang"],
        "appid": _config["appid"]
    }
    return requests.get(URL, args).text


def get_weather_icon_code(_data):
    weather = _data["weather"]
    return weather[0]["icon"]


def get_current_time():
    now = datetime.now()
    return now.strftime("%H%M")


def read_config():
    with open('config.json') as f:
        return json.load(f)


def help_config():
    print("You need to config the config.json. You can use the config.example.json as starting point")
    print("See https://openweathermap.org/current for valid config entries")


def display_resource(leds, image, x_offset=0, y_offset=0):
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
    leds.show()


def display_digit(leds, digit, x_offset=0, y_offset=0):
    image = Image.open(graphics.digit(digit))
    display_resource(leds, image, x_offset, y_offset)


def display_misc(leds, name, x_offset=0, y_offset=0):
    image = Image.open(graphics.misc(name))
    display_resource(leds, image, x_offset, y_offset)


def display_time(leds, time):
    colon_offset = 0
    for i in range(len(time)):
        if i == 2:
            display_misc(
                leds,
                "colon",
                x_offset=(i * graphics.DIGIT_IMAGE_WIDTH)
            )
            colon_offset = 2

        display_digit(
            leds,
            time[i],
            x_offset=(i * graphics.DIGIT_IMAGE_WIDTH) + colon_offset
        )


class Main:
    def signal_handler(self, sig, frame):
        self.matrix.finish()
        sys.exit(0)

    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)

        if platform.processor() != "x86_64":
            self.matrix = matrix.Matrix()
            display_time(self.matrix.leds, get_current_time())

        while True:
            pass


if __name__ == '__main__':
    print(platform.processor())
    config = read_config()
    json_text = request_weather(config)
    data = json.loads(json_text)

    code = get_weather_icon_code(data)
    print(code)

    Main()

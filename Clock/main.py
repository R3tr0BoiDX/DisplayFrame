import signal
import socket
import sys
import threading
import time

from PIL import Image
from rpi_ws281x import Color

import graphics
import matrix
import u131sync
import weather

REQUEST_DATA_INTERVAL = 120  # in seconds
UPDATE_INTERNET_STATUS_INTERVAL = 3  # in seconds

X_OFFSET_START = 2
Y_OFFSET_START = 0
X_OFFSET_WEATHER = 21

DAY_BRIGHTNESS = 16
NIGHT_BRIGHTNESS = 2

INTERNET_LED = (32, -8)  # todo: indexing in last column is broken
INTERNET_COLOR_DISCONNECTED = Color(255, 0, 0)  # red
INTERNET_COLOR_CONNECTED = Color(0, 0, 0)  # black


def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    By 7h3rAm from https://stackoverflow.com/a/33117579
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False


def get_current_time():
    now = time.localtime()
    return time.strftime("%H%M", now)


def get_current_brightness(_sun):
    now = int(time.time())
    if _sun[0] < now < _sun[1]:
        return DAY_BRIGHTNESS
    else:
        return NIGHT_BRIGHTNESS


def set_specific_led(leds, index, color, sync, render=True):
    print(color)
    print(sync.get_latest_color())

    matrix.set_pixel(index[0], index[1], color, leds)

    if render:
        leds.show()


def display_resource(leds, image, sync, x_offset=0, y_offset=0, render=True):
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


def display_digit(leds, digit, sync, x_offset=0, y_offset=0, render=True):
    image = Image.open(graphics.get_filepath(str(digit)))
    display_resource(leds, image, sync, x_offset, y_offset, render=render)


def display_weather(leds, code, sync, x_offset=0, y_offset=0, render=True):
    image = Image.open(graphics.get_filepath(code))
    display_resource(leds, image, sync, x_offset, y_offset, render=render)


def display_misc(leds, name, sync, x_offset=0, y_offset=0, render=True):
    image = Image.open(graphics.get_filepath(name))
    display_resource(leds, image, sync, x_offset, y_offset, render=render)


def display_time(leds, cur_time, sync, colon, render=True):
    matrix.flush(leds)

    colon_offset = 0
    for i in range(len(cur_time)):
        if i == 2:
            if colon:
                display_misc(
                    leds,
                    "colon",
                    sync,
                    x_offset=(i * graphics.DIGIT_IMAGE_WIDTH) + 1,
                    render=False
                )
            colon_offset = 2

        display_digit(
            leds,
            cur_time[i],
            sync,
            x_offset=(i * graphics.DIGIT_IMAGE_WIDTH) + colon_offset,
            render=False
        )

    if render:
        leds.show()


class Main:

    def show_time(self):
        display_time(self.matrix.leds, get_current_time(), self.colon, self.sync, render=False)
        self.colon = not self.colon

    def show_weather(self):
        display_weather(self.matrix.leds, self.weatherCode, self.sync, x_offset=X_OFFSET_WEATHER, render=False)

    def show_status_indicator(self):
        internet_status_color = INTERNET_COLOR_CONNECTED if self.internet_status else INTERNET_COLOR_DISCONNECTED
        set_specific_led(self.matrix.leds, INTERNET_LED, internet_status_color, self.sync, render=False)

    def set_current_brightness(self):
        matrix.set_brightness(get_current_brightness(self.sun), self.matrix.leds)

    def show_all(self):
        threading.Timer(1, self.show_all).start()
        self.show_time()
        self.show_weather()
        self.show_status_indicator()
        self.set_current_brightness()
        self.matrix.leds.show()

    def update_weather_and_sun(self):
        threading.Timer(REQUEST_DATA_INTERVAL, self.update_weather_and_sun).start()
        weather_and_sun = weather.get_weather_and_sun()
        self.weatherCode = weather_and_sun[0]
        self.sun = weather_and_sun[1]

    def update_internet_connection(self):
        threading.Timer(UPDATE_INTERNET_STATUS_INTERVAL, self.update_internet_connection).start()
        self.internet_status = check_internet_connection()

    def signal_handler(self, sig, frame):
        self.matrix.finish()
        sys.exit(0)

    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)

        self.colon = False
        self.internet_status = check_internet_connection()

        weather_and_sun = weather.get_weather_and_sun()
        self.weatherCode = weather_and_sun[0]
        self.sun = weather_and_sun[1]

        self.matrix = matrix.Matrix()
        self.show_all()
        self.update_weather_and_sun()

        self.sync = u131sync.U131Sync()


if __name__ == '__main__':
    Main()

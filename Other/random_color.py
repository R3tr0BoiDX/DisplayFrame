import random
import signal
import sys
import time

import _rpi_ws281x as ws281x
from rpi_ws281x import PixelStrip, Color

DELAY = 0

LED_HEIGHT = 8
LED_WIDTH = 32

TARGET_FREQ = ws281x.WS2811_TARGET_FREQ
GPIO_PIN = 18
DMA = 10
LED_COUNT = (LED_WIDTH * LED_HEIGHT)
STRIP_TYPE = ws281x.WS2812_STRIP
INVERTED = False
BRIGHTNESS = 2
CHANNEL = 0


def clear(leds):
    for i in range(leds.numPixels()):
        leds.setPixelColor(i, Color(0, 0, 0))
    leds.show()


def flush(leds):
    for i in range(leds.numPixels()):
        leds.setPixelColor(i, Color(0, 0, 0))


def setPixel(x, y, color, leds):
    leds.setPixelColor(ledMatrixTranslation(x, y), color)


def ledMatrixTranslation(x, y):
    if numberIsEven(x):
        return x * LED_HEIGHT + y
    else:
        return x * LED_HEIGHT + LED_HEIGHT - 1 - y


def numberIsEven(number):
    return number % 2 == 0


class Matrix:

    def __init__(self):
        # Create pixel object
        self.leds = PixelStrip(LED_COUNT, GPIO_PIN, TARGET_FREQ, DMA, INVERTED, BRIGHTNESS, CHANNEL,
                               strip_type=STRIP_TYPE)
        self.leds.begin()
        clear(self.leds)

    def finish(self):
        clear(self.leds)

    def signal_handler(self, sig, frame):
        self.finish()
        sys.exit(0)


def Main():
    matrix = Matrix()
    signal.signal(signal.SIGINT, matrix.signal_handler)

    while True:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        rgb = Color(r, g, b)

        x = random.randint(0, LED_WIDTH)
        y = random.randint(0, LED_HEIGHT)

        setPixel(x, y, rgb, matrix.leds)
        matrix.leds.show()
        time.sleep(DELAY)


if __name__ == '__main__':
    Main()

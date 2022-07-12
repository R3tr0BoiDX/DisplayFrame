import colorsys
import random
import signal
import sys
import time

import _rpi_ws281x as ws281x
from rpi_ws281x import PixelStrip, Color

DELAY = 0.002
INCREASE_COUNTER_LIMIT = 10

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

hue = 0
increase_counter = 0


# IDEA: use as background for clock
# pixel of clocks are inverted


def calc_next_hue():
    global hue
    global increase_counter
    if increase_counter < INCREASE_COUNTER_LIMIT:
        increase_counter += 1
    else:
        if hue < 255:
            hue += 1
        else:
            hue = 0
        increase_counter = 0


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


def main():
    matrix = Matrix()
    signal.signal(signal.SIGINT, matrix.signal_handler)

    while True:
        # get color
        calc_next_hue()
        color = colorsys.hsv_to_rgb((hue / 255), 1, 1)
        r = int(color[0] * 255)
        g = int(color[1] * 255)
        b = int(color[2] * 255)
        c = Color(r, g, b, )

        # get position
        x = random.randint(0, LED_WIDTH)
        y = random.randint(0, LED_HEIGHT)

        # show
        setPixel(x, y, c, matrix.leds)
        matrix.leds.show()
        time.sleep(DELAY)


if __name__ == '__main__':
    main()

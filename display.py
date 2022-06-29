import time
import _rpi_ws281x as ws281x
from rpi_ws281x import PixelStrip, Color

LED_HEIGHT = 8
LED_WIDTH = 32

TARGET_FREQ = ws281x.WS2811_TARGET_FREQ
GPIO_PIN = 18
DMA = 10
LED_COUNT = (LED_WIDTH * LED_HEIGHT)
STRIP_TYPE = ws281x.WS2812_STRIP
INVERTED = False
BRIGHTNESS = 24
CHANNEL = 0


def colorWipe(leds, color, wait_ms=50):
    for x in range(LED_WIDTH):
        for y in range(LED_HEIGHT):
            setPixel(x, y, color, leds)
            leds.show()
            time.sleep(wait_ms / 1000.0)


def clear(leds):
    for i in range(leds.numPixels()):
        leds.setPixelColor(i, Color(0, 0, 0))
    leds.show()


def setPixel(x, y, color, leds):
    leds.setPixelColor(ledMatrixTranslation(x, y), color)


def ledMatrixTranslation(_x, _y):
    if numberIsEven(_x):
        return _x * LED_HEIGHT + _y
    else:
        return _x * LED_HEIGHT + LED_HEIGHT - 1 - _y


def numberIsEven(_number):
    return _number % 2 == 0


class Display:

    def __init__(self):
        # Create pixel object
        self.leds = PixelStrip(
            LED_COUNT,
            GPIO_PIN,
            TARGET_FREQ,
            DMA,
            INVERTED,
            BRIGHTNESS,
            CHANNEL,
            strip_type=STRIP_TYPE
        )
        self.leds.begin()

    def finish(self):
        clear(self.leds)

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
BRIGHTNESS = 8
CHANNEL = 0


def clear(leds):
    for i in range(leds.numPixels()):
        leds.setPixelColor(i, Color(0, 0, 0))
    leds.show()


def flush(leds):
    for i in range(leds.numPixels()):
        leds.setPixelColor(i, Color(0, 0, 0))


def set_pixel(x, y, color, leds: PixelStrip):
    leds.setPixelColor(led_matrix_translation(x, y), Color(color[0], color[1], color[2]))


def set_brightness(brightness, leds):
    leds.setBrightness(brightness)


def led_matrix_translation(x, y):
    if number_is_even(x):
        return x * LED_HEIGHT + y
    else:
        return x * LED_HEIGHT + LED_HEIGHT - 1 - y


def number_is_even(number):
    return number % 2 == 0


class Matrix:

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
        clear(self.leds)

    def finish(self):
        clear(self.leds)

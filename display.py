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


def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


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
        if self.leds is not None:
            for i in range(self.leds.numPixels()):
                self.leds.setPixelColor(i, Color(0, 0, 0))
            self.leds.show()

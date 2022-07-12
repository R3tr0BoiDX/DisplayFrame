import random
import signal
import sys
import time

from rpi_ws281x import Color

from matrix import Matrix, set_pixel

DELAY = 33  # ms
FIRE_WIDTH = 32
FIRE_HEIGHT = 8

PALETTE = [
    (7, 7, 7),
    (31, 7, 7),
    (47, 15, 7),
    (71, 15, 7),
    (87, 23, 7),
    (103, 31, 7),
    (119, 31, 7),
    (143, 39, 7),
    (159, 47, 7),
    (175, 63, 7),
    (191, 71, 7),
    (199, 71, 7),
    (223, 79, 7),
    (223, 87, 7),
    (223, 87, 7),
    (215, 95, 7),
    (215, 95, 7),
    (215, 103, 15),
    (207, 111, 15),
    (207, 119, 15),
    (207, 127, 15),
    (207, 135, 23),
    (199, 135, 23),
    (199, 143, 23),
    (199, 151, 31),
    (191, 159, 31),
    (191, 159, 31),
    (191, 167, 39),
    (191, 167, 39),
    (191, 175, 47),
    (183, 175, 47),
    (183, 183, 47),
    (183, 183, 55),
    (207, 207, 111),
    (223, 223, 159),
    (239, 239, 199),
    (255, 255, 255)
]

pixels = []


def setup():
    # Set all pixes to black
    for i in range(FIRE_WIDTH * FIRE_HEIGHT):
        pixels.insert(i, 0)

    # Set bottom line to the highest possible color
    for i in range(FIRE_WIDTH):
        pixels[(FIRE_HEIGHT - 1) * FIRE_WIDTH + i] = len(PALETTE) - 1


def spread_fire(src):
    pixel = pixels[src]

    if pixel == 0:
        pixels[src - FIRE_WIDTH] = int(len(PALETTE) // 1.1)
    else:
        rand_idx = int(random.random() * 3) & 3
        dst = src - rand_idx + 1

        pixels[dst - FIRE_WIDTH] = pixel - (rand_idx & 1)


def do_fire():
    for x in range(FIRE_WIDTH):
        for y in range(FIRE_HEIGHT):
            spread_fire(y * FIRE_WIDTH + x)


# entry point
def main():
    setup()

    matrix = Matrix()
    signal.signal(signal.SIGINT, matrix.clear_and_exist)

    while True:
        do_fire()

        # draw pixel
        for x in range(FIRE_WIDTH):
            for y in range(FIRE_HEIGHT):
                index = abs(pixels[y * FIRE_WIDTH + x])
                if index >= len(PALETTE):
                    index = len(PALETTE) - 1

                pixel = PALETTE[index]
                r = int(pixel[0])
                g = int(pixel[1])
                b = int(pixel[2])
                color = Color(r, g, b, )

                set_pixel(x, y, color, matrix.leds)

        matrix.leds.show()
        time.sleep(DELAY / 1000)


if __name__ == '__main__':
    main()

    # likely never reached
    sys.exit()

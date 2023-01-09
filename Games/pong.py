import random
import socket
import threading
import time

import bit_ops
import matrix

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

CLOCK_SPEED = 0.1  # s


def get_input(sock):
    print("start thread")
    while True:
        data, addr = sock.recvfrom(1)
        control = int.from_bytes(data, byteorder='big', signed=False)
        print(control)

        if not bit_ops.check_bit(control, 0):
            print("player 0")

            if bit_ops.check_bit(control, 1):
                print("up")

            if bit_ops.check_bit(control, 2):
                print("down")

            if bit_ops.check_bit(control, 3):
                print("left")

            if bit_ops.check_bit(control, 4):
                print("right")

            if bit_ops.check_bit(control, 5):
                print("a")

            if bit_ops.check_bit(control, 6):
                print("b")

            if bit_ops.check_bit(control, 7):
                print("start")


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    threading.Thread(target=get_input, args=(sock,)).start()

    display = matrix.Matrix().leds

    white = (255, 255, 255)

    offset_horizontal = 2
    offset_vertical = 1

    game_over = False

    ball_pos_x = matrix.LED_WIDTH // 2
    ball_pos_y = matrix.LED_HEIGHT // 2

    ball_dir_x = random.choice([-1, 1])
    ball_dir_y = random.choice([-1, 1])
    while not game_over:
        matrix.clear(display)
        matrix.set_pixel((ball_pos_x, ball_pos_y), white, display)

        ball_pos_x += (1 * ball_dir_x)
        ball_pos_y += (1 * ball_dir_y)

        if ball_pos_x > matrix.LED_WIDTH - offset_horizontal - 1 or ball_pos_x < offset_horizontal + 1:
            ball_dir_x *= -1

        if ball_pos_y > matrix.LED_HEIGHT - offset_vertical - 1 or ball_pos_y < offset_vertical + 1:
            ball_dir_y *= -1

        display.show()
        time.sleep(CLOCK_SPEED)


if __name__ == '__main__':
    main()

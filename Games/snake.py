import socket
import threading
import time

import matrix
import bit_ops

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

CLOCK_SPEED = 0.010  # s


def get_input(sock):
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

    game_over = False

    ball_pos = (16, 4)
    while not game_over:
        matrix.set_pixel(ball_pos, white, display)

        ball_pos = tuple(value + 1 for value in ball_pos)

        display.show()
        time.sleep(CLOCK_SPEED)


if __name__ == '__main__':
    main()

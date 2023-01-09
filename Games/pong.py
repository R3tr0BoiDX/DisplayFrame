import random
import socket
import threading
import time

import bit_ops
import matrix

UDP_PORT = 5005
CLOCK_SPEED = 0.5  # s

WHITE = (255, 255, 255)


class Input:

    def __init__(self):
        self.current_input = 0

    def get_input(self, sock):
        while True:
            data, addr = sock.recvfrom(1)
            control = int.from_bytes(data, byteorder='big', signed=False)

            if control == 1 or control == 2:  # only care about ups and downs, lul
                self.current_input = bit_ops.combine(self.current_input, control)


def main():
    # setup thread
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', UDP_PORT))

    # setup input class
    recv_input = Input()
    threading.Thread(target=recv_input.get_input, args=(sock,)).start()

    # setup display
    display = matrix.Matrix().leds

    # ball
    ball_offset_horizontal = 3
    ball_offset_vertical = 1

    ball_pos_x = matrix.LED_WIDTH // 2
    ball_pos_y = matrix.LED_HEIGHT // 2

    ball_dir_x = random.choice([-1, 1])
    ball_dir_y = random.choice([-1, 1])

    # player
    player_height = 2
    player_offset_x = ball_offset_horizontal - 1

    player_one_pos_y = matrix.LED_HEIGHT // 2

    game_over = False
    while not game_over:
        matrix.flush(display)

        # draw ball
        matrix.set_pixel((ball_pos_x, ball_pos_y), WHITE, display)

        if ball_pos_x > matrix.LED_WIDTH - ball_offset_horizontal - 1 or ball_pos_x < ball_offset_horizontal + 1:

            if ball_dir_x > 0:
                if ball_pos_y == player_one_pos_y or ball_pos_y == player_one_pos_y + 1:
                    print("coll")
                else:
                    print("miss")
            else:
                if ball_pos_y == player_one_pos_y or ball_pos_y == player_one_pos_y + 1:
                    print("coll")
                else:
                    print("miss")

            ball_dir_x *= -1

        if ball_pos_y > matrix.LED_HEIGHT - ball_offset_vertical - 2 or ball_pos_y < ball_offset_vertical + 2:
            ball_dir_y *= -1

        ball_pos_x += (1 * ball_dir_x)
        ball_pos_y += (1 * ball_dir_y)

        # player one
        if bit_ops.check_bit(recv_input.current_input, 0):  # up
            recv_input.current_input = bit_ops.clear_bit(recv_input.current_input, 0)
            if player_one_pos_y > ball_offset_vertical:
                player_one_pos_y -= 1

        if bit_ops.check_bit(recv_input.current_input, 1):  # down
            recv_input.current_input = bit_ops.clear_bit(recv_input.current_input, 1)
            if player_one_pos_y < matrix.LED_HEIGHT - ball_offset_vertical - player_height:
                player_one_pos_y += 1

        for i in range(0, player_height):
            matrix.set_pixel((player_offset_x, player_one_pos_y + i), WHITE, display)

        # todo: player two
        for i in range(0, player_height):
            matrix.set_pixel((matrix.LED_WIDTH - player_offset_x, player_one_pos_y + i), WHITE, display)

        # game logic
        display.show()
        time.sleep(CLOCK_SPEED)


if __name__ == '__main__':
    main()

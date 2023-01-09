import random
import socket
import threading
import time

import bit_ops
import matrix

UDP_PORT_PLAYER_ONE = 5004
UDP_PORT_PLAYER_TWO = 5005
CLOCK_SPEED = 0.1  # s

WHITE = (255, 255, 255)

BLINK_COUNT_GAME_OVER = 3
BLINK_DELAY_GAME_OVER = 0.5  # ms


class Input:

    def __init__(self):
        self.current_input = 0

    def get_input(self, sock):
        while True:
            data, addr = sock.recvfrom(1)
            control = int.from_bytes(data, byteorder='big', signed=False)
            self.current_input = bit_ops.combine(self.current_input, control)


def main():
    # setup player one input
    sock_p1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_p1.bind(('', UDP_PORT_PLAYER_ONE))
    input_p1 = Input()
    threading.Thread(target=input_p1.get_input, args=(sock_p1,)).start()

    # setup player two input
    sock_p2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_p2.bind(('', UDP_PORT_PLAYER_TWO))
    input_p2 = Input()
    threading.Thread(target=input_p2.get_input, args=(sock_p2,)).start()

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

    # duplicate
    matrix.set_pixel((ball_pos_x, ball_pos_y), WHITE, display)
    for i in range(0, player_height):
        matrix.set_pixel((player_offset_x, player_one_pos_y + i), WHITE, display)

    # todo: player two
    for i in range(0, player_height):
        matrix.set_pixel((matrix.LED_WIDTH - player_offset_x, player_one_pos_y + i), WHITE, display)
    # end duplicat


    # wait for either player to press start
    display.show()
    while not bit_ops.check_bit(input_p1.current_input, 64) and not bit_ops.check_bit(input_p2.current_input, 64):
        print("wait for start to be pressed")
        time.sleep(0.5)


    game_over = False
    while not game_over:
        matrix.flush(display)

        # draw ball
        matrix.set_pixel((ball_pos_x, ball_pos_y), WHITE, display)

        # check collision and switch direction horizontally
        if ball_pos_x > matrix.LED_WIDTH - ball_offset_horizontal - 1 or ball_pos_x < ball_offset_horizontal + 1:

            missed = True
            if ball_dir_x < 0:
                for i in range(0, player_height):
                    if ball_pos_y == player_one_pos_y + i:
                        ball_dir_x *= -1
                        missed = False

            else:
                for i in range(0, player_height):
                    if ball_pos_y == player_one_pos_y + i:  # todo: player two
                        ball_dir_x *= -1
                        missed = False

            game_over = missed

        # switch direction vertically
        if ball_pos_y > matrix.LED_HEIGHT - ball_offset_vertical - 2 or ball_pos_y < ball_offset_vertical + 2:
            ball_dir_y *= -1

        # move ball
        ball_pos_x += (1 * ball_dir_x)
        ball_pos_y += (1 * ball_dir_y)

        # player one
        if bit_ops.check_bit(input_p1.current_input, 0):  # up
            input_p1.current_input = bit_ops.clear_bit(input_p1.current_input, 0)
            if player_one_pos_y > ball_offset_vertical:
                player_one_pos_y -= 1

        if bit_ops.check_bit(input_p1.current_input, 1):  # down
            input_p1.current_input = bit_ops.clear_bit(input_p1.current_input, 1)
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

    matrix.blink(BLINK_COUNT_GAME_OVER, BLINK_DELAY_GAME_OVER, display)
    print("game over")


if __name__ == '__main__':
    main()

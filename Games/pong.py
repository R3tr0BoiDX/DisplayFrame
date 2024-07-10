import logging
import random
import time

import matrix
import network_gamepad

CLOCK_SPEED = 0.1  # s

BLINK_COUNT_ROUND_OVER = 1
BLINK_DELAY_ROUND_OVER = 0.5  # ms

BLINK_COUNT_GAME_OVER = 3
BLINK_DELAY_GAME_OVER = 0.5  # ms

BALL_OFFSET_HORIZONTAL = 3
BALL_OFFSET_VERTICAL = 1

PLAYER_HEIGHT = 2
PLAYER_OFFSET_X = BALL_OFFSET_HORIZONTAL - 1

POINTS_POS_MIN_Y = 6

WHITE = (255, 255, 255)


class Pong:

    def __init__(self, input_p1, input_p2):
        self.input_p2 = input_p2
        self.input_p1 = input_p1
        self.p2_points = None
        self.p1_points = None
        self.display = None
        self.p2_pos_y = None
        self.p1_pos_y = None
        self.ball_dir_y = None
        self.ball_dir_x = None
        self.ball_pos_y = None
        self.ball_pos_x = None

    def reset_ball_pos(self):
        self.ball_pos_x = matrix.LED_WIDTH // 2
        self.ball_pos_y = matrix.LED_HEIGHT // 2

        self.ball_dir_x = random.choice([-1, 1])
        self.ball_dir_y = random.choice([-1, 1])

    def reset_player_pos(self):
        self.p1_pos_y = matrix.LED_HEIGHT // 2
        self.p2_pos_y = matrix.LED_HEIGHT // 2

    def reset_points(self):
        self.p1_points = 0
        self.p2_points = 0

    def render_ball(self):
        matrix.set_pixel((self.ball_pos_x, self.ball_pos_y), WHITE, self.display)

    def render_player(self):
        for i in range(PLAYER_HEIGHT):
            matrix.set_pixel((PLAYER_OFFSET_X, self.p1_pos_y + i), WHITE, self.display)

        for i in range(PLAYER_HEIGHT):
            matrix.set_pixel((matrix.LED_WIDTH - PLAYER_OFFSET_X, self.p2_pos_y + i), WHITE,
                             self.display)

    def render_points(self):
        for i in range(self.p1_points):
            matrix.set_pixel((0, POINTS_POS_MIN_Y - i), WHITE, self.display)
        for i in range(self.p2_points):
            matrix.set_pixel((matrix.LED_WIDTH - 1, POINTS_POS_MIN_Y - i), WHITE, self.display)  # todo: indexing bug

    def wait_for_start(self):
        while not network_gamepad.check_bit(self.input_p1.current_input, 6) and not network_gamepad.check_bit(
                self.input_p2.current_input, 6):
            time.sleep(CLOCK_SPEED)

        # clear start
        self.input_p1.current_input = network_gamepad.clear_bit(self.input_p1.current_input, 6)
        self.input_p2.current_input = network_gamepad.clear_bit(self.input_p2.current_input, 6)

    def check_collision(self, player_pos_y):
        for i in range(PLAYER_HEIGHT):
            if self.ball_pos_y == player_pos_y + i:
                self.ball_dir_x *= -1
                return False
        return True

    def get_input(self):
        if network_gamepad.check_bit(self.input_p1.current_input, 0):  # up
            self.input_p1.current_input = network_gamepad.clear_bit(self.input_p1.current_input, 0)
            if self.p1_pos_y > BALL_OFFSET_VERTICAL:
                self.p1_pos_y -= 1

        if network_gamepad.check_bit(self.input_p1.current_input, 1):  # down
            self.input_p1.current_input = network_gamepad.clear_bit(self.input_p1.current_input, 1)
            if self.p1_pos_y < matrix.LED_HEIGHT - BALL_OFFSET_VERTICAL - PLAYER_HEIGHT:
                self.p1_pos_y += 1

    def play(self):
        # setup display
        self.display = matrix.Matrix().leds

        # setup ball
        self.reset_ball_pos()

        # setup player
        self.reset_player_pos()
        self.reset_points()

        # init render
        self.render_ball()
        self.render_player()
        self.display.show()

        # wait for either player to press start
        self.wait_for_start()

        # main loop
        round_over = False
        while True:
            while not round_over:
                matrix.flush(self.display)

                # draw ball
                matrix.set_pixel((self.ball_pos_x, self.ball_pos_y), WHITE, self.display)

                # check collision, give points and switch direction horizontally
                if self.ball_pos_x > matrix.LED_WIDTH - BALL_OFFSET_HORIZONTAL - 1 or self.ball_pos_x < BALL_OFFSET_HORIZONTAL + 1:

                    if self.ball_dir_x < 0:
                        missed = self.check_collision(self.p1_pos_y)
                        if missed:
                            self.p2_points += 1

                    else:
                        missed = self.check_collision(self.p2_pos_y)
                        if missed:
                            self.p1_points += 1

                    round_over = missed

                # switch direction vertically
                if self.ball_pos_y > matrix.LED_HEIGHT - BALL_OFFSET_VERTICAL - 2 or self.ball_pos_y < BALL_OFFSET_VERTICAL + 2:
                    self.ball_dir_y *= -1

                # move ball
                self.ball_pos_x += (1 * self.ball_dir_x)
                self.ball_pos_y += (1 * self.ball_dir_y)

                # player one
                self.get_input()

                # render
                self.render_player()
                self.render_points()
                self.display.show()

                # game tick
                time.sleep(CLOCK_SPEED)

            # round over. reset and start next round
            matrix.blink(BLINK_COUNT_ROUND_OVER, BLINK_DELAY_ROUND_OVER, self.display)

            self.reset_ball_pos()
            self.reset_player_pos()

            # win condition
            if self.p1_points == 3 or self.p2_points == 3:
                break

            # wait for either player to press start
            self.wait_for_start()
            round_over = False

        matrix.blink(BLINK_COUNT_GAME_OVER, BLINK_DELAY_GAME_OVER, self.display)

        # wait for either player to press start
        self.wait_for_start()
        matrix.clear(self.display)


if __name__ == '__main__':
    # setup player input
    p1 = network_gamepad.setup_input(network_gamepad.UDP_PORT_PLAYER_ONE)
    p2 = network_gamepad.setup_input(network_gamepad.UDP_PORT_PLAYER_TWO)

    # start game
    Pong(p1, p2).play()

    # kill threads
    logging.info("Stop threads")
    p1.stop()
    p2.stop()

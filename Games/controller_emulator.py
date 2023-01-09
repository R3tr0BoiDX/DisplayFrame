import socket

import pygame

from Games.bit_ops import set_bit

# pixel map:
# 0 - up
# 1 - down
# 2 - left
# 3 - right
# 4 - a
# 5 - b
# 6 - start
# 7 - select

SIZE = (256, 224)
UDP_IP = "192.168.2.102"
UDP_PORT = 5004

pygame.init()
dis = pygame.display.set_mode(SIZE)
pygame.display.update()
pygame.display.set_caption("Controller emulator")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            val = 0

            if event.key == pygame.K_UP:
                val = set_bit(val, 0)
                print("player 1: up")
            if event.key == pygame.K_DOWN:
                val = set_bit(val, 1)
                print("player 1: down")
            if event.key == pygame.K_LEFT:
                val = set_bit(val, 2)
                print("player 1: left")
            if event.key == pygame.K_RIGHT:
                val = set_bit(val, 3)
                print("player 1: right")
            if event.key == pygame.K_a:
                val = set_bit(val, 4)
                print("player 1: a")
            if event.key == pygame.K_s:
                val = set_bit(val, 5)
                print("player 1: b")
            if event.key == pygame.K_RETURN:
                val = set_bit(val, 6)
                print("player 1: start")
            if event.key == pygame.K_SPACE:
                val = set_bit(val, 7)
                print("player 1: select")

            sock.sendto(val.to_bytes(1, byteorder='big', signed=False), (UDP_IP, UDP_PORT))
            print('final bitmap: {}={:b}'.format(val, val))

pygame.quit()
quit()

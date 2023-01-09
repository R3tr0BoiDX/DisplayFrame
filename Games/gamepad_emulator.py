import socket

import pygame

import network_gamepad

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
                val = network_gamepad.set_bit(val, 0)
                print("player: up")
            if event.key == pygame.K_DOWN:
                val = network_gamepad.set_bit(val, 1)
                print("player: down")
            if event.key == pygame.K_LEFT:
                val = network_gamepad.set_bit(val, 2)
                print("player: left")
            if event.key == pygame.K_RIGHT:
                val = network_gamepad.set_bit(val, 3)
                print("player: right")
            if event.key == pygame.K_a:
                val = network_gamepad.set_bit(val, 4)
                print("player: a")
            if event.key == pygame.K_s:
                val = network_gamepad.set_bit(val, 5)
                print("player: b")
            if event.key == pygame.K_RETURN:
                val = network_gamepad.set_bit(val, 6)
                print("player: start")
            if event.key == pygame.K_SPACE:
                val = network_gamepad.set_bit(val, 7)
                print("player: select")

            sock.sendto(val.to_bytes(1, byteorder='big', signed=False), (UDP_IP, UDP_PORT))
            print('final bitmap: {}={:b}'.format(val, val))

pygame.quit()
quit()

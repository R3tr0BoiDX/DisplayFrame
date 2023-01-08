import logging
import socket

from .. import matrix


def draw_at_index(color, index, display: matrix.Matrix):
    y = index // matrix.LED_WIDTH
    x = index % matrix.LED_WIDTH

    matrix.set_pixel(x, y, color, display)


def receive_datagrams(display):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the address and port
    server_address = ('localhost', 19446)
    sock.bind(server_address)

    # Receive the message
    data, client_address = sock.recvfrom(4096)

    parse_datagram(data, display)


def parse_datagram(datagram, display):
    data = []
    for byte in datagram:
        data.append(byte)

    logging.debug(f"Mode: {data[0]}")
    logging.debug(f"Timeout: {data[1]}")

    pixel = []
    for i in range(2, len(data), 3):
        logging.debug(f"R: {data[i]}, G: {data[i + 2]}, B: {data[i + 1]}")
        pixel.append([data[i + 0], data[i + 2], data[i + 1]])

    for i in range(0, len(pixel)):
        draw_at_index(pixel[i], i, display)


if __name__ == '__main__':
    leds = matrix.Matrix()
    while True:
        receive_datagrams(leds)

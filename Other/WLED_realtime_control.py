import logging
import socket

import matrix


def receive_datagrams(recv_sock, display):
    # Receive the message
    data, client_address = recv_sock.recvfrom(4096)

    logging.debug("Received datagram")
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

    display.leds.show()


def draw_at_index(color, index, display: matrix.Matrix):
    y = index // matrix.LED_WIDTH
    x = index % matrix.LED_WIDTH

    logging.debug(f"Set {x}{y} to R: {color[0]}, G: {color[1]}, B: {color[2]}")

    matrix.set_pixel(x, y, color, display.leds)


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    # Create a LED matrix
    leds = matrix.Matrix()

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logging.info("Created socket")

    # Bind the socket to the address and port
    server_address = ('', 19446)
    sock.bind(server_address)
    logging.info("Bound socket")

    while True:
        receive_datagrams(sock, leds)

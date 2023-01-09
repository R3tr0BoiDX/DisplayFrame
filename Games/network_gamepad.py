import socket
import threading


def set_bit(value, bit):
    return value | (1 << bit)


def clear_bit(value, bit):
    return value & ~(1 << bit)


def check_bit(x, n):
    return x & (1 << n)


def combine(a, b):
    return a | b


def setup_input(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))
    recv_input = Input()
    threading.Thread(target=recv_input.get_input, args=(sock,)).start()
    return recv_input


class Input:
    def __init__(self):
        self.current_input = 0

    def get_input(self, sock):
        while True:
            data, addr = sock.recvfrom(1)
            control = int.from_bytes(data, byteorder='big', signed=False)
            self.current_input = combine(self.current_input, control)

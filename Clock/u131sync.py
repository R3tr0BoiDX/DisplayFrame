import socket
import threading

PORT = 5568


def get_values(self, sock):
    while True:
        # Receive the data
        data, address = sock.recvfrom(1024)

        # Put the data into array
        recv_bytes = []
        for byte in data:
            recv_bytes.append(byte)

        # Last three elements are the color
        self.red = recv_bytes[-3]
        self.green = recv_bytes[-2]
        self.blue = recv_bytes[-1]


class U131Sync:

    def __init__(self):
        self.red = 255
        self.green = 255
        self.blue = 255

        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Allow reuse of the socket
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the broadcast address and port
        sock.bind(('', 5568))

        threading.Thread(target=get_values, args=(self, sock,)).start()

    def get_latest_color(self):
        return self.red, self.green, self.blue


if __name__ == '__main__':
    U131Sync()

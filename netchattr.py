import socket
import threading
import time
from faker import Faker
import os
import random
import argparse


class Netchattr:
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('localhost', port))
        self.faker = Faker()
        self.name = self.faker.user_name()
        print(f"Starting netchattr \'{
            self.name}\' on port {port}\n")

    def send_message(self):
        ports = range(5000, 5100)  # Define the range of ports here
        while True:
            message = self.faker.sentence()
            for port in ports:
                if port != self.sock.getsockname()[1]:
                    self.sock.sendto(
                        f'{self.name.upper()}: {message}\n'.encode(), ('localhost', port))
            time.sleep(random.randint(2, 5))

    def receive_message(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            print(data.decode())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a netchattr instance.')
    parser.add_argument(
        'port', type=int, help='The port number to use for this instance.')

    args = parser.parse_args()

    netchattr = Netchattr(args.port)
    # No need to pass args.port here
    threading.Thread(target=netchattr.send_message).start()
    threading.Thread(target=netchattr.receive_message).start()

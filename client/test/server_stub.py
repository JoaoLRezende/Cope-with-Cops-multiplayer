"""A small program that serves messages from
a text file.
"""

import socket
from sys import argv
from time import sleep


def _get_port_num():
    """Get the port number the user passed in the command line.
    """
    # Find the argument that contains the port number.
    for argument in argv:
        """If this argument is a digit string, then
        it's probably the port number. ¯\_(ツ)_/¯
        """
        if argument.isdecimal():
            return int(argument)

class ClientInfo:
    def __init__(self, id, socket):
        self.socket = socket
        self.received_text = ""
        self.id = id

    def _update_received_text(self):
        try:
            self.received_text += str(self.socket.recv(4096), encoding="utf-8")
        except BlockingIOError:
            pass

    def receive_messages(self):
        self._update_received_text()
        while "\n" in self.received_text:
            message, _, self.received_text = self.received_text.partition("\n")
            if message:
                print(f"Received from {self.id}: {message}")
                yield message

    def receive_specific_message(self, expected_message):
        self._update_received_text()
        message, _, self.received_text = self.received_text.partition("\n")
        if message == expected_message:
            return message
        else:
            exit(f"Expected {expected_message} from {self.id} but received {message}")


    def send_message(self, message):
        self.socket.send((message + "\n").encode())
        print(f"Sent to {self.id}: {message}")


def main():
    listening_socket = socket.socket()
    listening_socket.bind(("localhost", _get_port_num()))
    listening_socket.listen()

    cop = ClientInfo(0, listening_socket.accept()[0])
    cop.send_message("HELLO 0")

    fugitive = ClientInfo(1, listening_socket.accept()[0])
    fugitive.send_message("HELLO 1")
    cop.send_message("FUGITIVEREADY")
    cop.receive_specific_message("INIT")

    for client in (cop, fugitive):
        client.socket.setblocking(False)
        client.send_message("INIT")

    while True:
        latest_MV_messages = [None, None]
        for client in (cop, fugitive):
            for message in client.receive_messages():
                if message[:2] == "MV":
                    latest_MV_messages[client.id] = message
        if latest_MV_messages[1]: cop.send_message(latest_MV_messages[1])
        if latest_MV_messages[0]: fugitive.send_message(latest_MV_messages[0])


main()

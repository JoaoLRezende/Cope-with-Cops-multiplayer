"""A small program that serves messages from
a text file.
"""

import socket
from sys import argv
from time import sleep


FILE_NAME = "test_messages.txt"


def _get_port_num():
    """Get the port number the user passed in the command line.
    """
    # Find the argument that contains the port number.
    for argument in argv:
        """If this argument's first character is a digit, then
        it's probably the port number. ¯\_(ツ)_/¯
        """
        if argument[0].isdecimal():
            return int(argument)

_raw_received_text = ""

def main():
    listening_socket = socket.socket()
    listening_socket.bind(("localhost", _get_port_num()))
    listening_socket.listen()

    while True:
        connected_socket, client_address = listening_socket.accept()
        connected_socket.setblocking(False)
        messages_file = open(FILE_NAME, "r")
        time_between_messages = 0
        for line in messages_file:
            if line[0] == "#" or len(line) < 2:
                pass
            elif line[0:6] == "\wait ":
                sleep(float(line[6:]))
            elif line[0:9] == "\waitall ":
                time_between_messages = float(line[9:])
            else:
                connected_socket.send(line.encode())
                print("Sent:", line, end = "")
                sleep(time_between_messages)
        
            global _raw_received_text
            try:
                _raw_received_text += str(connected_socket.recv(4096), encoding="utf-8")
            except BlockingIOError:
                pass
            while "\n" in _raw_received_text:
                message, _, _raw_received_text = _raw_received_text.partition("\n")

                if message:
                    print("Received: ", message)

try:
    main()
except (ConnectionResetError, BrokenPipeError):
    pass
"""A small program that serves messages from
a text file.
"""

import socket
from sys import argv


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


def main():
    listening_socket = socket.socket()
    listening_socket.bind(("localhost", _get_port_num()))
    listening_socket.listen()

    while True:
        connected_socket, client_address = listening_socket.accept()
        messages_file = open(FILE_NAME, "rb")
        connected_socket.sendfile(messages_file)
        

main()
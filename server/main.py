import socket


def main():
    listening_socket = socket.socket()
    listening_socket.bind(("localhost", 8008))
    listening_socket.listen()

    while True:
        connected_socket, client_address = listening_socket.accept()
        messages_file = open("test_messages.txt", "rb")
        connected_socket.sendfile(messages_file)
        
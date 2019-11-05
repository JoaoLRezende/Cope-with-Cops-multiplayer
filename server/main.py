from common.constants import *
from common.car import Car
import server.transit as transit
import socket

game_is_running = True
cars_per_latitude = 1

cop_car = None
fugitive_car = None

def main():
    cop_car = Car(CAR_HEIGHT + 1, ROAD_WIDTH / 2, 7, is_cop_car = True)
    bandit = Car(CAR_HEIGHT + 30, ROAD_WIDTH / 2, 7, is_cop_car = False)
    listening_socket = socket.socket()
    listening_socket.bind(("localhost", 8008))
    listening_socket.listen()

    while game_is_running:
        transit.add_transit_cars(latitude, cars_per_latitude)
        connected_socket, client_address = listening_socket.accept()
        messages_file = open("test_messages.txt", "rb")
        connected_socket.sendfile(messages_file)
        
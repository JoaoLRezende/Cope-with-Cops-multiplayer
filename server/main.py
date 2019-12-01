"""A small program that serves messages from
a text file.
"""
import socket
from sys import argv
from time import sleep
from random import random
from common.constants import *


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

def _get_diff_num():
    """Get the port number the user passed in the command line.
    """
    # Find the argument that contains the port number.
    for argument in argv:
        """If this argument is a single digit string, then
        it's probably the difficulty. ¯\_(ツ)_/¯
        """
        if argument.isdecimal() and int(argument) > 0 and int(argument) < 4:
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
    listening_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    port = _get_port_num()
    hostName = socket.gethostbyname( '0.0.0.0' )
    listening_socket.bind(("", _get_port_num()))
    listening_socket.listen()
    print("Server is running, waiting for players")
    cop = ClientInfo(0, listening_socket.accept()[0])
    cop.send_message("HELLO 0")

    fugitive = ClientInfo(1, listening_socket.accept()[0])
    fugitive.send_message("HELLO 1")
    cop.send_message("FUGITIVEREADY")
    cop.receive_specific_message("INIT")

    
    for client in (cop, fugitive):
        client.socket.setblocking(False)
        client.send_message("INIT")
    distance_between_players = INITIAL_FUGITIVE_DISTANCE_FROM_COP
    difficulty = _get_diff_num()
    current_distance_until_next_batch = 0
    game_is_running = True
    latest_height = [None,None]
    highest_latitude = 20
    chance_to_spawn = 0.5
    while game_is_running:
        current_max_car_per_row = difficulty * 2
        vertical_distance_between_cars = (abs( difficulty - 3) + 1) * 2
        
        
        latest_MV_messages = [None, None]
        
        for client in (cop, fugitive):
            for message in client.receive_messages():
                if message[:2] == "MV":
                    latest_MV_messages[client.id] = message
                elif message[:4] == "BOOM":
                        if client.id == 1:
                            cop.send_message("DED")
                            game_is_running = False
                            for client in (cop, fugitive):
                                client.socket.close()
                            listening_socket.close
                            exit()
                            exit()
                        else:
                            fugitive.send_message("DED")
                            game_is_running = False
                            for client in (cop, fugitive):
                                client.socket.close()
                            listening_socket.close
                            exit()
                        
                elif message[:7] == "CAPTURE":
                    fugitive.send_message("CAPTURED")
                    game_is_running = False
                    exit()

        if latest_MV_messages[1]:
            cop.send_message(latest_MV_messages[1])
            print(int((latest_MV_messages[1].partition(" ")[2]).partition(" ")[0]))
            latest_height[1] = int((latest_MV_messages[1].partition(" ")[2]).partition(" ")[0])
            if int((latest_MV_messages[1].partition(" ")[2]).partition(" ")[0]) > highest_latitude:
                highest_latitude = int((latest_MV_messages[1].partition(" ")[2]).partition(" ")[0])
                if(current_distance_until_next_batch == 0):
                    chance_to_spawn = chance_to_spawn + 1/(2 * difficulty)
                    if chance_to_spawn > 0.8:
                        chance_to_spawn = 0.8
                    for row in range(current_max_car_per_row):
                        if(random() > chance_to_spawn):
                            color = str(round(1+random() * 7))
                            while (color == "1" or color == "6"):
                                color = str(round(1 + random() * 7))
                            new_car_message = "SPAWNNPC " + str(highest_latitude+60) + " " + str(round(random() * (ROAD_WIDTH - CAR_WIDTH-1))) + " " + color
                            for client in (cop, fugitive):
                                client.send_message(new_car_message)
                        current_distance_until_next_batch = vertical_distance_between_cars + 1
                current_distance_until_next_batch -=1
                #print(current_distance_until_next_batch, highest_latitude)


        if latest_MV_messages[0]: 
            fugitive.send_message(latest_MV_messages[0])
            print(int((latest_MV_messages[0].partition(" ")[2]).partition(" ")[0]))
            latest_height[0] = int((latest_MV_messages[0].partition(" ")[2]).partition(" ")[0])
            if int((latest_MV_messages[0].partition(" ")[2]).partition(" ")[0]) > highest_latitude:
                highest_latitude = int((latest_MV_messages[0].partition(" ")[2]).partition(" ")[0]) 
                if(current_distance_until_next_batch == 0):
                    for row in range(current_max_car_per_row):
                        if(random() > 0.5):
                            color = str(round(1+random() * 7))
                            while color == "1" or color == "6":
                                color = str(round(1 + random() * 7))
                            new_car_message = "SPAWNNPC " + str(highest_latitude+60) + " " + str(round(random() * (ROAD_WIDTH - CAR_WIDTH-1))) + " " + color
                            for client in (cop, fugitive):
                                client.send_message(new_car_message)
                        current_distance_until_next_batch = vertical_distance_between_cars + 1
                current_distance_until_next_batch -=1
        if(latest_height[0] and latest_height[1]):
            distance_between_players = abs(latest_height[0] - latest_height[1])
        if distance_between_players > difficulty * 333:
            for client in (cop, fugitive):
                client.send_message("FREEDOM")
                client.socket.close()
            listening_socket.close
            exit()

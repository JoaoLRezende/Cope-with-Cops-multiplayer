"""
A possible implementation:
In the beginning of each game tick, this module's get_new_events function
is called from the main loop.
receive_events then receives new data from the server and returns a container
with that data that has each kind of data accessible through a different
attribute, for consumtion by the other modules.
"""

import socket

from common.constants import *
from common.car       import Car
from sys import exit    # temp


server_socket = None


def init():
    global server_socket
    server_socket = socket.socket(type = (socket.SOCK_STREAM))
    server_socket.connect(("localhost", 8009))
    server_socket.setblocking(False)



class Event:
    def __init__(self):
        """Only one of these attributes will hold a non-None value,
        depending on what type of event this object carries.
        """
        self.new_transit_car = None

_raw_received_text = ""
def _receive_events():
    """Generator that parses incoming event strings and yields event objects.
    
    Returns when there aren't any more full event strings to parse.
    """
    global _raw_received_text
    try:
        _raw_received_text += str(server_socket.recv(4096), encoding="utf-8")
    except BlockingIOError:
        pass

    while "\n" in _raw_received_text:
        message, _, _raw_received_text = _raw_received_text.partition("\n")

        if message and message[0] == "t":
            new_transit_car_event = Event()
            car_parameters = message[1:].split(",")
            new_transit_car_event.new_transit_car = Car(
                latitude   =      int(car_parameters[0]),
                longitude  =      int(car_parameters[1]),
                color      =      int(car_parameters[2]),
                is_cop_car = bool(int(car_parameters[3]))
            )
            yield new_transit_car_event
            

def get_new_events():
    class EventsContainer():
        def __init__(self):
            self.new_transit = None

    new_events = EventsContainer()

    for event in _receive_events():

        """If event is a new transit car, add it to new_events's new_transit
        linked list of cars, which is to be delivered
        as a 2-element list [first_car, last car].
        """
        if hasattr(event, "new_transit_car"):
            if not new_events.new_transit:
                new_events.new_transit = [event.new_transit_car,
                                          event.new_transit_car]
            else:
                new_events.new_transit[1].next_car = event.new_transit_car
                new_events.new_transit[1]          = event.new_transit_car
    return new_events


    from random import randrange
    from client.rendering import colors
    for latitude in range(5, 500, 2):
        car = Car(latitude, randrange(ROAD_WIDTH - CAR_WIDTH),
                  colors[randrange(1, len(colors))])
        transit.add_car(car)


def debug_msg(message):
    """Send a message to be shown in the server's console.
    """
    pass    # TODO
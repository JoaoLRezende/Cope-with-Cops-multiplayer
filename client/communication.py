import socket
from sys import argv
from sys import exit
from common.constants import *
from common.car       import Car


server_socket = None


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


class Event:
    """Instances of this class encapsulate the events returned by
    _receive_events.
    """
    def __init__(self):
        """Only one of these attributes will hold a non-None value,
        depending on what type of event the object carries.
        """
        self.player_id = None
        self.new_transit_car = None


"""_raw_received_text contains received text that still hasn't been
broken into separate messages. It is manipulated only by _receive_events.
"""
_raw_received_text = ""

def _receive_events():
    """Generator that parses incoming messages and yields Event objects.
    
    Returns when there aren't any more full messages to parse.
    """
    # Update _raw_received_text with new inbound text, if there is any.
    global _raw_received_text
    try:
        _raw_received_text += str(server_socket.recv(4096), encoding="utf-8")
    except BlockingIOError:
        pass

    # While there is at least one full message to parse, parse it.
    while "\n" in _raw_received_text:
        message, _, _raw_received_text = _raw_received_text.partition("\n")
        if message:
            """If the first word in the message is HELLO, then we are
            receiving our ID as part of the initialization procedure.
            """
            if message[:5] == "HELLO":
                player_id_event = Event()
                player_id_event.player_id = int(message[5:])
                yield player_id_event
                """We return after yielding this event,
                since we don't want to receive anything else yet.
                """
                return

            """If the first word in the message is "SPAWNNPC"; i.e., if it is
            a new transit car we're receiving.
            """
            if message[0:8] == "SPAWNNPC":
                new_transit_car_event = Event()
                car_parameters = message[9:].split(" ")
                new_transit_car_event.new_transit_car = Car(
                    latitude   =      int(car_parameters[0]),
                    longitude  =      int(car_parameters[1]),
                    color      =      int(car_parameters[2]),
                    is_cop_car = bool(int(car_parameters[3]))
                )
                yield new_transit_car_event


def init():
    global server_socket
    server_socket = socket.socket(type = socket.SOCK_STREAM)
    server_socket.connect(("localhost", _get_port_num()))

    player_id = None
    """Get the event from _receive_events containing our ID received
    in a HELLO message. (_receive_events will yield nothing
    but that event. The body of the for loop below will be executed only once.)
    """
    for player_id_event in _receive_events():
        player_id = player_id_event.player_id
    assert player_id is not None

    server_socket.setblocking(False)


def get_new_events():
    """Get an object containing all events received since the last tick.
    
    This is the function that gets called at the beginning of each tick
    from the game's main loop.
    It takes events from _receive_events and further encapsulates them in
    a container that accumulates each kind of data in a different
    attribute, for consumtion by the other modules.
    """
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


def debug_msg(message):
    """Send a message to be shown in the server's console.
    """
    pass    # TODO
_cop_socket = None
_fugitive_socket = None

def init():
    listening_socket = socket.socket()
    listening_socket.bind(("localhost", 8008))
    listening_socket.listen()

class Event:
    """Instances of this class encapsulate the events returned by
    _receive_events.
    """
    def __init__(self):
        """Only one of these attributes will hold a non-None value,
        depending on what type of event the object carries.
        """
        self.new_player_position = None


"""_raw_received_text contains received text that still hasn't been
broken into separate messages. It is manipulated only by _receive_events.
"""
_raw_received_text = ""

def _receive_events():
    """Generator that parses incoming messages and yields event objects.
    
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

            """If the first word in the message is a "SPAWNNPC"; i.e., if it is
            a new transit car we're receiving.
            """
            if message[0:8] == "SPAWNNPC":
                new_transit_car_event = Event()
                car_parameters = message[1:].split(" ")
                new_transit_car_event.new_transit_car = Car(
                    latitude   =      int(car_parameters[0]),
                    longitude  =      int(car_parameters[1]),
                    color      =      int(car_parameters[2]),
                    is_cop_car = bool(int(car_parameters[3]))
                )
                yield new_transit_car_event
        

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

def send_car(car):
    for socket in (_cop_socket, _fugitive_socket):
        socket.send(      "SPAWNNPC "
                    + car.id        + " "
                    + car.latitude  + " "
                    + car.longitude + " "
                    + car.color     + "\n")

def spawn_player(car, target):
    if target == "cop":
        socket = _cop_socket
    else:
        socket = _fugitive_socket
    
        socket.send(      "SPAWNPLAYER "
                    + car.id        + " "
                    + car.latitude  + " "
                    + car.longitude + " "
                    + car.color     + "\n")
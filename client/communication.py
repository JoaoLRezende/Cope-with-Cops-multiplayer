"""
A possible implementation:
In the beginning of each game tick, this module's get_new_events function
is called in the main loop.
receive_events then receives new data from the server and returns a container
with that data that has each kind of data accessible through a different
attribute, for consumtion by the other modules.
"""

from common.constants import *
from common.car       import Car



class Event:
    pass

class NewTransitCarEvent(Event):
    def __init__(self):
        self.new_transit_car = None

def _receive_events():
    """Generator that parses incoming event strings and yields event objects.
    
    Returns when there aren't any more full event strings to parse.
    """
    event = NewTransitCarEvent()
    event.new_transit_car = Car(CAR_HEIGHT + PLAYER_DISTANCE_FROM_BOTTOM + 5, ROAD_WIDTH // 2 + 5, 7, is_cop_car = True)
    yield event



def get_new_events():
    class EventsContainer():
        def __init__(self):
            self.new_transit = None

    new_events = EventsContainer()

    for event in _receive_events():
        """If event is a new transit car, add it to new_events's new_transit
        linked list of cars, which is to be delivered
        as a 2-tuple (first_car, last car).
        """
        if isinstance(event, NewTransitCarEvent):
            if not new_events.new_transit:
                new_events.new_transit = (event.new_transit_car,
                                          event.new_transit_car)
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
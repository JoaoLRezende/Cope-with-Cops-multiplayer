import client.communication
from common.constants import *

from client.render import debug_print   # temp

"""
Our transit is a linked list of cars.
_transit_back maintains a reference to the car that has the lowest latitude.
Each car has a reference to the car that has the lowest latitude
that is greater than its own.
"""
_transit_back  = None
_transit_front = None


"""
add_car is to be called by the communication module when the server
spawns a new car.
"""
def add_car(car):
    debug_print("Receiving car from server at latitude %d." % car.latitude, 5)
    global _transit_back, _transit_front
    if not _transit_front:
        _transit_back  = car
        _transit_front = car
        return
    _transit_front.next_car = car
    _transit_front = car


"""
get_visible_cars creates an iterator that feeds the cars that are to be
drawn on the screen.
It also eliminates from our transit cars we'be already passed.
"""
def get_visible_cars(maximum_visible_latitude):
    debug_print("hi")
    class Iterator():
        def __iter__(self):
            return self
        def __init__(self, transit_back, maximum_visible_latitude):
            self.current_car = transit_back
            self.maximum_visible_latitude = maximum_visible_latitude
        def __next__(self):
            current_car = self.current_car
            if not current_car or (current_car.latitude - (CAR_HEIGHT - 1) >
                                   maximum_visible_latitude):
                raise StopIteration
            self.current_car = current_car.next_car
            return current_car
    return Iterator(_transit_back, maximum_visible_latitude)

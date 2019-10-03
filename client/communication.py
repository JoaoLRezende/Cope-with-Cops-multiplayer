"""
This module could act synchronously (being called in every iteration
of the main looop) or asynchronously (in a separate thread). Idk.
"""

import client.transit as transit

from client.render import debug_print   # temp

"""
One of the things this module should do is call transit's add_car whenever a new
car arrives from the server.
Below is a test stub that pretends to receive many cars at once.
"""
def totally_receive_cars_from_the_server():
    from random import randrange
    from common.car import Car
    from common.constants import ROAD_WIDTH
    from client.render import colors
    for latitude in range(5, 500, 3):
        car = Car(latitude, randrange(ROAD_WIDTH),
                  colors[randrange(1, len(colors))])
        transit.add_car(car)

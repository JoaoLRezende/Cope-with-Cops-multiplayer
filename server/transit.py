from common.constants import *
from common.car import Car
from random import randrange
import curses


_transit_back  = None
_transit_front = None

colors = [
            0,                    # An empty element to occupy position 0.

            # car colors
            curses.COLOR_BLACK,   # 1
            curses.COLOR_BLUE,    # 2
            curses.COLOR_CYAN,    # 3
            curses.COLOR_GREEN,   # 4
            curses.COLOR_MAGENTA, # 5
            curses.COLOR_RED,     # 6
            curses.COLOR_WHITE,   # 7
            curses.COLOR_YELLOW   # 8
            ]

def random_car(latitude, cars_per_latitude):
    carros_novos = []
    for i in range(0, cars_per_latitude):
        new_car = Car(latitude, randrange(ROAD_WIDTH - CAR_WIDTH),
                      colors[randrange(1, len(colors))])
        _transit_front.next_car = new_car    
        _transit_front = new_car
        carros_novos.append(new_car)

def create_car_barrier(max_longitude):
    carros_novos = []
    first_car = Car(0, 0,
                    colors[randrange(1, len(colors))])
    _transit_back = first_car
    _transit_front = first_car
    carros_novos.append(first_car)

    for i in range(1, max_longitude):
        new_car = Car(0, i,
                      colors[randrange(1, len(colors))])
        _transit_front.next_car = new_car    
        _transit_front = new_car
        carros_novos.append(new_car)


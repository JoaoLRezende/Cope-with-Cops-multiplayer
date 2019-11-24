""" Stuff related to how stuff is shown on the screen in general. """

import curses
from sys import exit
from time import time

from common.constants import *


"""Constant attributes initialized by the init function.
See that function for details.
"""
colors = None
_screen = None
_road = None



def _paint_cell(row, column, color_index, window = None,
               character = None, attributes = 0):
    """Write a given character into a given cell with a given color.

    Also allows determining other attributes to be ORed with the
    color attribute. This function doesn't refresh the window.
    """
    if not character:
        character = curses.ACS_BOARD
    if not window:
        window = _road

    attributes |= curses.color_pair(color_index)
    if (row < 0 or row >= window.getmaxyx()[0]
            or column < 0 or column >= window.getmaxyx()[1]):
        return
    window.addch(row, column, character, attributes)


def _create_road_view():
    """Draw the edges of the road and initialize road_view.

    Each cell of the edge is painted by writing a space character in it with
    the attribute attr.
    """
    left_edge_column  = (_screen.getmaxyx()[1] - MIN_SCREEN_WIDTH) // 2
    right_edge_column = left_edge_column + 1 + ROAD_WIDTH
    for j in [left_edge_column, right_edge_column]:
        for i in range(_screen.getmaxyx()[0]):
            _paint_cell(i, j, colors.index(curses.COLOR_BLACK), _screen)

    _screen.refresh()

    return curses.newwin(_screen.getmaxyx()[0], ROAD_WIDTH,
                         0, left_edge_column + 1)


def init(screen):
    global _screen, _road, colors

    _screen = screen
    curses.curs_set(0)

    """A list of colors used throughout the game. These are passed to curses
    in this order before the game starts. Colors are then referenced through
    their indices.
    The first element is skipped so that indices of colors in this list
    coincide with the indices of their respective color pairs as maintained
    internally by curses. (Color pair 0 isn't used for painting: it is
    the white-black pair, and can't be changed.) To get the index of the color
    pair corresponding to a named color, then, colors.index(color)
    becomes a useful idiom.
    """
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

    """Initialize curses' color pairs with the colors above.
    Each color pair has the same color for text and background,
    because, in gnome-terminal, the color of a cell painted with the
    curses.ACS_BOARD character seems to be a mixture of the two.
    """
    for color_index in range(1, len(colors)):
        curses.init_pair(color_index, colors[color_index], colors[color_index])

    _road = _create_road_view()
    
    return _screen


def _update_cop_siren_lights(cop, max_visible_latitude):
    if time() - cop.time_of_last_siren_flip > COP_SIREN_PERIOD:

        if cop.current_siren_colors[0] == colors.index(curses.COLOR_RED):
            cop.current_siren_colors = (colors.index(curses.COLOR_BLUE),
                                        colors.index(curses.COLOR_RED))
        else:
            cop.current_siren_colors = (colors.index(curses.COLOR_RED),
                                        colors.index(curses.COLOR_BLUE))

        cop.time_of_last_siren_flip = time()

    _paint_cell(max_visible_latitude - (cop.latitude_int() - CAR_HEIGHT//2),
                cop.longitude_int(),
                cop.current_siren_colors[0])

    _paint_cell(max_visible_latitude - (cop.latitude_int() - CAR_HEIGHT//2),
                cop.longitude_int() + CAR_WIDTH - 1,
                cop.current_siren_colors[1])


def get_maximum_visible_latitude(player_car):
    """Calculate the world latitude that corresponds to the topmost row.

    Takes the player's car to use as a reference point.
    """
    return player_car.latitude_int() + (_road.getmaxyx()[0]
                                        - PLAYER_DISTANCE_FROM_BOTTOM
                                        - CAR_HEIGHT)


def _draw_car(car, max_visible_latitude):
    for latitude in range (car.latitude_int(),
                           car.latitude_int() - CAR_HEIGHT, -1):
        for longitude in range (car.longitude_int(),
                                car.longitude_int() + CAR_WIDTH):
            _paint_cell(max_visible_latitude - latitude, longitude, car.color)

    if car.is_cop_car:
        _update_cop_siren_lights(car, max_visible_latitude)
        

def draw_scene(player_car, other_car, visible_transit_cars):
    _road.erase()

    maximum_visible_latitude = get_maximum_visible_latitude(player_car)

    _draw_car(player_car, maximum_visible_latitude)
    _draw_car(other_car, maximum_visible_latitude)

    for car in visible_transit_cars:
        _draw_car(car, maximum_visible_latitude)

    _road.refresh()

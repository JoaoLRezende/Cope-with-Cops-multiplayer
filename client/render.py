""" Stuff related to how stuff is shown on the screen in general. """

import curses
import random

from common.constants import *
from common.car import Car # temp (we shouldn't need to create instances of Car here)


"""
A list of colors used throughout the game. These are passed to curses
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

"""
Initialize curses' color pairs with the colors above.
Each color pair has the same color for text and background,
because, in gnome-terminal, the color of a cell painted with the
curses.ACS_BOARD character seems to be a mixture of the two.
"""
for color_index in range(1, len(colors)):
    curses.init_pair(color_index, colors[color_index], colors[color_index])


""" Make the cursor invisible. """
curses.curs_set(0)



# _road_view will hold a reference to the curses window representing the road.
_road_view = None


"""
paint_cell writes a given character into a given cell with a given color.
Also allows determining other attributes to be ORed with the color attribute.
This function doesn't refresh the window.
"""
def paint_cell(row, column, color_index, window = None,
               character = curses.ACS_BOARD, attributes = 0):
    attributes |= curses.color_pair(color_index)
    if not window: window = _road_view
    if (row < 0 or row >= window.getmaxyx()[0]
            or column < 0 or column >= window.getmaxyx()[1]):
        return
    window.addch(row, column, character, attributes)


"""
create_road_view draws the edges of the road and initializes road_view.
Each cell of the edge is painted by writing a space character in it with
the attribute attr.
"""
def create_road_view(screen):
    left_edge_column  = (screen.getmaxyx()[1] - ROAD_WIDTH - 2) // 2
    right_edge_column = left_edge_column + 1 + ROAD_WIDTH
    for j in [left_edge_column, right_edge_column]:
        for i in range(screen.getmaxyx()[0]):
            paint_cell(i, j, colors.index(curses.COLOR_BLACK), screen)
    global _road_view
    _road_view = curses.newwin(screen.getmaxyx()[0], ROAD_WIDTH,
                              0, left_edge_column + 1)
    screen.refresh()


def draw_car(car, maximum_visible_latitude):
    try:
        for latitude in range (car.latitude, car.latitude - CAR_HEIGHT, -1):
            for longitude in range (car.longitude, car.longitude + CAR_WIDTH):
                paint_cell(maximum_visible_latitude - latitude, longitude, car.color)
    except:
        debug_print("There was an error drawing a car.", 1000)      # FIXME. This seems to be caused by attempts to draw cars that intersect with the right edge of the road.

def get_maximum_visible_latitude(player_car):
    return player_car.latitude + (_road_view.getmaxyx()[0]
                                  - PLAYER_DISTANCE_FROM_BOTTOM
                                  - CAR_HEIGHT)


def draw_cars(player_car, visible_transit_cars):
    _road_view.erase()
    maximum_visible_latitude = player_car.latitude + (_road_view.getmaxyx()[0]
                                                      - PLAYER_DISTANCE_FROM_BOTTOM
                                                      - CAR_HEIGHT)
    draw_car(player_car, maximum_visible_latitude)
    for car in visible_transit_cars:
        draw_car(car, maximum_visible_latitude)
    _road_view.refresh()


# temp
last_debug_line = 0
def debug_print(message, nap_after_printing = 0):
    global last_debug_line
    _road_view.addstr(last_debug_line, 0, message)
    _road_view.refresh()
    curses.napms(nap_after_printing)
    if nap_after_printing < 0:
        _road_view.getch()
    last_debug_line = (last_debug_line + 1) % _road_view.getmaxyx()[0]

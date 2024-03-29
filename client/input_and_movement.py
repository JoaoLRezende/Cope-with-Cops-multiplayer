from sys import exit, argv
from time import time
import curses

from common.constants import *

from client.communication import debug_msg

"""
We load and use the keyboard module only if either we're root
or we're on Windows.
After we do, we keep a reference to it in keyboard.
"""
keyboard = None

"""
Else, we read keyboard input through standard input with curses.
(Note that this results in much less smooth steering.)
In that case, we keep a reference to the game's main window object in screen.
"""
screen = None

time_of_last_tick = 0

_up    = "up"
_down  = "down"
_left  = "left"
_right = "right"


def _should_use_keyboard():
    from platform import system

    if system() == "Windows":
        return True
        
    if system() == "Linux":
        from os import getuid
        # if we're the root user
        if getuid() == 0:
            return True

    else:
        return False


def _initialize_keys():
    global _up, _down, _left, _right
    if "--wasd" in argv:
        _up   = "w"
        _down = "s"
        _left = "a"
        _right = "d"


def init(player_car, screen_window):
    player_car.velocity = INITIAL_VELOCITY

    if _should_use_keyboard():
        from importlib import import_module
        global keyboard
        try:
            keyboard = import_module("keyboard")
        except ImportError:
            exit("Please install the keyboard module as root:\n"
                 "\tsudo python3 -m pip install keyboard")
    else:
        exit("run with sudo pls")     # TODO: make curses support decent, then remove this line
        global screen
        screen = screen_window
        screen.nodelay(True)

    _initialize_keys()


def read_input_and_update_player(player_car):
    global time_of_last_tick

    current_time = time()
    time_since_last_tick = current_time - time_of_last_tick
    time_of_last_tick = current_time

    player_car.latitude += player_car.velocity * time_since_last_tick

    if keyboard:
        if   keyboard.is_pressed(_left):  player_car.longitude += -1
        elif keyboard.is_pressed(_right): player_car.longitude += +1

        if player_car.longitude < 0:
            player_car.longitude = 0
        if player_car.longitude >= ROAD_WIDTH - CAR_WIDTH:
            player_car.longitude = ROAD_WIDTH - CAR_WIDTH

        intended_vertical_directon  =  1 if keyboard.is_pressed(_up)   else 0
        intended_vertical_directon += -1 if keyboard.is_pressed(_down) else 0
        # If the player is pressing up or down.
        if intended_vertical_directon:
            # If the player is trying to increase their vertical speed.
            if intended_vertical_directon * player_car.velocity >= 0:
                player_car.velocity += (intended_vertical_directon
                                        * PEDAL_ACCELERATION
                                        * time_since_last_tick)
            # If the player is braking.
            elif intended_vertical_directon * player_car.velocity < 0:
                player_car.velocity += (intended_vertical_directon
                                        * BRAKE_DECELERATION
                                        * time_since_last_tick)
        # If the player is not pressing up nor down.
        else:
            speed_decrement = ((1 if player_car.velocity < 0 else -1)
                               * IDLE_DECELERATION
                               * time_since_last_tick)

            if abs(player_car.velocity) < abs(speed_decrement):
                player_car.velocity = 0
            else:
                player_car.velocity += speed_decrement
    
    else:
        input = screen.getch()

        """Flush the input buffer because, in the next call to this function,
        we'll want only input that has been entered since now. We don't
        want to accumulate input.
        """
        curses.flushinp()

        if input == curses.KEY_LEFT:
            player_car.longitude += -1
        elif input == curses.KEY_RIGHT:
            player_car.longitude +=  1

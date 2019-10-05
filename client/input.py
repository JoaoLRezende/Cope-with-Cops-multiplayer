from sys import exit
import curses

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

def should_use_keyboard():
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


def init(screen_window):
    if should_use_keyboard():
        from importlib import import_module
        global keyboard
        try:
            keyboard = import_module("keyboard")
        except ImportError:
            exit("Please install the keyboard module as root:\n"
                 "\tsudo python3 -m pip install keyboard")
    else:
        global screen
        screen = screen_window
        screen.nodelay(True)


def read_input_and_update_player(player_car):
    if keyboard:
        if keyboard.is_pressed("left"):  player_car.longitude += -1
        if keyboard.is_pressed("right"): player_car.longitude += +1
    
    else:
        input = screen.getch()

        """
        Flush the input buffer because, in the next call to this function,
        we'll want only input that has been entered since now. We don't
        want to accumulate input.
        """
        curses.flushinp()

        if input == curses.KEY_LEFT:
            player_car.longitude += -1
        elif input == curses.KEY_RIGHT:
            player_car.longitude +=  1
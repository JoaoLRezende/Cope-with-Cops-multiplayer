import curses

screen = None

def init(screen_window):
    global screen
    screen = screen_window
    screen.nodelay(True)


def read_input_and_update_player(player_car):
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
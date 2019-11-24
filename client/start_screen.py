import curses
import curses.textpad as textpad


def print_string_centralized(window, string):
    window.erase()
    lines = string.splitlines()
    initial_row_number = (window.getmaxyx()[0] // 2) - (len(lines) // 2)
    for (row_number, line) in enumerate(lines, initial_row_number):
        column = (window.getmaxyx()[1] // 2) - (len(line) // 2)
        window.addstr(row_number, column, line)
    window.refresh()


def request_resize(window, min_height, min_width):
    while(window.getmaxyx()[0] < min_height or
          window.getmaxyx()[1] < min_width):
        print_string_centralized(window,
                                  "Please maximize your terminal window.")
        window.getch()
    window.erase()

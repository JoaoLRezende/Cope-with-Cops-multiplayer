from common.constants import *
from curses import napms
from time import time, sleep

time_of_last_tick_start = 0

def sleep_until_next_tick():
    global time_of_last_tick_start

    time_since_last_tick_start = time() - time_of_last_tick_start

    if time_since_last_tick_start < MIN_TICK_INTERVAL:
        sleep(MIN_TICK_INTERVAL - time_since_last_tick_start)

    time_of_last_tick_start = time()

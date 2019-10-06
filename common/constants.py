### configurable values ###

MIN_SCREEN_HEIGHT = 40
ROAD_WIDTH = 130

CAR_HEIGHT = 3
CAR_WIDTH  = 2

PLAYER_DISTANCE_FROM_BOTTOM = 10

MAX_FPS = 15

INITIAL_SPEED = 0     # in cells per second

COP_SIREN_PERIOD = .05      # in seconds


### derived constants ###

MIN_SCREEN_WIDTH = ROAD_WIDTH + 2

# The minimum amount of time that must pass between ticks, in seconds. (#TODO: enforce this.)
MIN_TICK_INTERVAL = 1 / MAX_FPS
### configurable values ###

MIN_SCREEN_HEIGHT = 40
ROAD_WIDTH = 130

CAR_HEIGHT = 3
CAR_WIDTH  = 2

PLAYER_DISTANCE_FROM_BOTTOM = 10

MAX_FPS = 30

INITIAL_VELOCITY = 0     # in cells per second

# The speed-increase rate when the player presses up,
# in cells per second per second.
PEDAL_ACCELERATION = 70
# The speed-decrease rate when the player isn't pressing anything.
IDLE_DECELERATION =  20
# The speed-decrease rate when the player presses down while moving forwards.
BRAKE_DECELERATION = 100

COP_SIREN_PERIOD = .05      # in seconds


### derived constants ###

MIN_SCREEN_WIDTH = ROAD_WIDTH + 2

# The minimum amount of time that must pass between ticks, in seconds. (#TODO: enforce this.)
MIN_TICK_INTERVAL = 1 / MAX_FPS
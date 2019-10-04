from curses import napms        # temp

from common.constants import *
import client.start_screen as start_screen
import client.timing as timing
from common.car import Car

def main(screen):
    import client.rendering as rendering
    import client.input as input
    import client.communication as communication
    import client.transit as transit

    start_screen.request_resize(screen, MIN_SCREEN_HEIGHT, MIN_SCREEN_WIDTH)
    road_view = rendering.create_road_view(screen)
    input.init(screen)
    communication.totally_receive_cars_from_the_server()
    player_car = Car(CAR_HEIGHT + PLAYER_DISTANCE_FROM_BOTTOM,
                     ROAD_WIDTH // 2, 6)
    while True:
        input.read_input_and_update_player(player_car)
        other_cars = transit.get_visible_cars(rendering.get_maximum_visible_latitude(player_car))
        rendering.draw_cars(player_car, other_cars)
        transit.check_for_collision(player_car)

        player_car.latitude += 1
        timing.sleep_until_next_tick()

    napms(5000)

from curses import napms        # temp

from common.constants import *
import client.start_screen as start_screen
from common.car import Car

def main(screen):
    import client.render as render
    import client.communication as communication
    import client.transit as transit
    start_screen.request_resize(screen, MIN_SCREEN_HEIGHT, MIN_SCREEN_WIDTH)
    road_view = render.create_road_view(screen)
    communication.totally_receive_cars_from_the_server()
    player_car = Car(CAR_HEIGHT + PLAYER_DISTANCE_FROM_BOTTOM,
                     ROAD_WIDTH // 2, 6)
    while True:
        other_cars = transit.get_visible_cars(render.get_maximum_visible_latitude(player_car))
        render.draw_cars(player_car, other_cars)
        transit.check_for_collision(player_car)

        player_car.latitude += 1
        napms(30)


    napms(5000)

from sys import exit
from common.constants import *
from common.car import Car
import client.start_screen       as start_screen
import client.tick_rate_control  as tick_rate_control
import client.rendering          as rendering
import client.input_and_movement as input_and_movement
import client.communication      as communication
import client.transit            as transit

def main(screen):
    start_screen.request_resize(screen, MIN_SCREEN_HEIGHT, MIN_SCREEN_WIDTH)
    
    player_id = communication.init()

    cop_car = Car(CAR_HEIGHT + PLAYER_DISTANCE_FROM_BOTTOM,
                  ROAD_WIDTH // 2, 7, is_cop_car = True)
    fugitive_car = Car(CAR_HEIGHT + PLAYER_DISTANCE_FROM_BOTTOM + INITIAL_FUGITIVE_DISTANCE_FROM_COP,
                       ROAD_WIDTH // 2, 6, is_cop_car = False)
    if player_id == 0:
        player_car, other_car = cop_car, fugitive_car
    elif player_id == 1:
        player_car, other_car = fugitive_car, cop_car

    input_and_movement.init(player_car, screen)

    if player_id == 0:
        start_screen.print_string_centralized(screen,
            "You are the cop.\n\nWaiting for a criminal to chase.\n\n"
        )
        communication.wait_for_fugitive_ready()
        start_screen.print_string_centralized(screen,
            "You are the cop.\n\nWe have a fugitive.\n" +
            "Press any key to start the game."
        )
        screen.getch()
        communication.send("INIT")
    elif player_id == 1:
        start_screen.print_string_centralized(screen,
            "You are the fugitive.\n\nWaiting for the cop to start the game.")
    
    communication.wait_for_init()

    rendering.init(screen)

    
    while True:
        input_and_movement.read_input_and_update_player(player_car)

        communication.send_position(player_car)

        new_events = communication.get_new_events()

        if new_events.other_car_position:
            other_car.latitude, other_car.longitude = \
                                                  new_events.other_car_position

        transit.update_transit(new_events)

        visible_transit_cars = transit.get_visible_cars(
            rendering.get_maximum_visible_latitude(player_car)
        )
        rendering.draw_scene(player_car, other_car, visible_transit_cars)

        transit.check_for_collision(player_car)
        if player_id == 0 and transit.are_cars_colliding(player_car, other_car):
            communication.send("CAPTURE")
            exit("You captured the fugitive! You won the game.")

        tick_rate_control.sleep_until_next_tick()
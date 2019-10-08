class Car:
    def __init__(self, latitude, longitude, color, next_car = None, is_cop_car = False):
        self.latitude   = latitude     # latitude  of the car's top-left cell
        self.longitude  = longitude    # longitude of the car's top-left cell
        self.color      = color        # index of the car's color
        
        self.next_car   = next_car

        self.is_cop_car = is_cop_car
        self.time_of_last_siren_flip = 0
        self.current_siren_colors = (None, None)

    """
    Even though a each cell of the screen has integer coordinates while
    the coordinates of a car can be fractional,
    for drawing and collision-detection purposes, each car is regarded
    as occupying only a set of exactly CAR_HEIGHT*CAR_WIDTH cells.
    (No cell is "half-occupied".)
    Thus, for those purposes, instances of Car provide methods that return an
    approximation of the car's exact position as an integer.
    """
    def latitude_int(self):  return round(self.latitude)
    def longitude_int(self): return round(self.longitude)

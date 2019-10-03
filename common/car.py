class Car:
    def __init__(self, latitude, longitude, color, next_car = None):
        self.latitude     = latitude     # latitude  of the car's top-left cell
        self.longitude    = longitude    # longitude of the car's top-left cell
        self.color        = color        # index of the car's color
        self.next_car = next_car
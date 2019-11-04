Only a very simple client-server communication test is currently implemented.
To run it, use

    python3 __main__.py --server

to start a server and then

    sudo python3 __main__.py

to run a client instance.


TODO:
- fix the "curses function returned NULL" that appears when the player's window isn't big enough.
- use the argparse module to take the server's IP address and port number as arguments in the command line.
- implement a very barebones server that allows receiving debug messages from the client.
- we might want to use this deleted piece of code somewhere to generate random cars:
    from random import randrange
    from client.rendering import colors
    for latitude in range(5, 500, 2):
        car = Car(latitude, randrange(ROAD_WIDTH - CAR_WIDTH),
                  colors[randrange(1, len(colors))])
        transit.add_car(car)

- create a command-line option that makes you able to control your car with the ADWS keys. This would let you play as two players from the same PC.
- prevent the rendering functions from trying to draw (i.e. passing to draw_car) cars whose latitude is is lower than the minimum visible latitude, for efficiency.
- implement proper accelerating and breaking.
- some cars spawn with the same color as the background. Either make the background a unique color or prevent cars from being that color.
- make everything independent from the tick frequency. (cars' speed shouldn't be influenced by it, for example.)
- in this readme file, describe everything the user should know about running the game as the root user and how that affects controls if you're on Linux. (see comments in the input module and in the documentation of the keyboard module itself.)
- module attributes that shouldn't be visible from other modules should have a name beginning with an underscore, as per PEP 8.
- make sure all the cool parts of the original Cope with Cops are here. (Including explosions and stuff. But without the annoying hey-look-this-explosion-is-so-cool pause. Also make explosions grow outwards while gradually fading.)
- make sure the thing works on most PCs. (Make sure it works on Windows too. Also make sure smooth steering − through the keyboard module − is always used there, since it doesn't require administrative privileges there.)
- make the transit increasingly more dense as time passes. (After a while, it should force all players to go really slowly.)
- consider that the server doesn't need to generate transit cars in a purely random manner. It could occasionaly spawn some barriers of cars or (maybe some maze-like stuff) or other obstacles that force the drivers to slow down.
- study the documentation for the socket module and ip(7), tcp(7), socket(7) and other related man pages and see if there's anything useful there we should be using or considering.

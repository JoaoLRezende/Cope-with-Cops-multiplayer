To run the game, use ```python3 .``` or ```python3 __main__.py```.

Not sure what exactly to implement yet. Some ideas:
- same thing as in the original game, but with one of the players controlling the cop car. (Maybe the player controlling the cop car should have a very short view distance. Or maybe make him only able to see cars that he would actually be able to see.)
- something very similar to the original game, but in which two players are chased simultaneously by two cop cars. (Maybe make the two players able to support each other in some way.)
- a street race. No cops. (But then you'd need to be able to accelerate and brake and stuff.)

TODO:
- implement a very barebones server that allows receiving debug messages from the client.
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
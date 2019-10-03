To run the game, use ```python3 .``` or ```python3 __main__.py```.

Not sure what exactly to implement yet. Some ideas:
- same thing as in the original game, but with one of the players controlling the cop car. (Maybe the player controlling the cop car should have a very short view distance. Or maybe make him only able to see cars that he would actually be able to see.)
- something very similar to the original game, but in which two players are chased simultaneously by two cop cars. (Maybe make the two players able to support each other in some way.)
- a street race. No cops. (But then you'd need to be able to accelerate and brake and stuff.)

Some arbitrary observations:
- We might somewhere want to have a linked list (perhaps called ```transit```) of the non-playable cars on the road.
Cars in that list will be ordered by their vertical distance from the game’s starting point (which we might call their latitude). (This ordering will minimize the time we spend traversing that list in each tick period in order to find visible cars.) Each car descriptor in that list will store that distance and also its horizontal distance from the left edge of the road (which we might call its longitude).
The server will dynamically, proactively create cars a while before they appear on the clients' screens. It will notify all clients of those cars as they are created.

TODO:
- make colors work. learn precisely how you will use the curses.ACS_BOARD character to pain cells. (experiment in some external code.) then review all the color-related code you've already written. then: make the printRoadView function receive a color for the road's edges. (and then finish that function)
- build a fundamental framework for the game. Make classes for cars, car drawing, steering, the transit list.
- maybe some of the modules should be classes instead.
- the size of the terminal window should probably be captured when gameplay starts. (After the connection is established.)
- use decent steering controls.
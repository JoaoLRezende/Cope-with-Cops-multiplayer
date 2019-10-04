To run the game, use ```python3 .``` or ```python3 __main__.py```.

Not sure what exactly to implement yet. Some ideas:
- same thing as in the original game, but with one of the players controlling the cop car. (Maybe the player controlling the cop car should have a very short view distance. Or maybe make him only able to see cars that he would actually be able to see.)
- something very similar to the original game, but in which two players are chased simultaneously by two cop cars. (Maybe make the two players able to support each other in some way.)
- a street race. No cops. (But then you'd need to be able to accelerate and brake and stuff.)

TODO:
- some cars spawn with the same color as the background. Either make the background a unique color or prevent cars from being that color.
- implement steering.
- implement reading keyboard input through the keyboard module (https://pypi.org/project/keyboard/) (which should be much smoother) − but make it optional, since it requires root.
- make everything independent from the tick frequency. (cars' speed shouldn't be influenced by it, for example.)
- maybe some of the modules should be classes instead.
- fix the import mess. move imports to the top of source files. initialize modules in an intialization function; not on import.
- make sure all the cool parts of the original Cope with Cops are here. (Including explosions and stuff.)
- make sure the thing works on most PCs. (Make sure it works on Windows too. Also make sure smooth steering − through the keyboard module − is always used there, since it doesn't require administrative privileges there.)
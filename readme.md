To run the game, use ```python3 .``` or ```python3 __main__.py```.

Not sure what exactly to implement yet. Some ideas:
- same thing as in the original game, but with one of the players controlling the cop car. (Maybe the player controlling the cop car should have a very short view distance. Or maybe make him only able to see cars that he would actually be able to see.)
- something very similar to the original game, but in which two players are chased simultaneously by two cop cars. (Maybe make the two players able to support each other in some way.)
- a street race. No cops. (But then you'd need to be able to accelerate and brake and stuff.)

TODO:
- in the rendering module, the code that deals with mapping latitudes do screen rows is confusing. Encapsulate the code that does this in a properly commented function.
- implement a very barebones server that allows receiving debug messages from the client.
- implement proper accelerating and breaking.
- some cars spawn with the same color as the background. Either make the background a unique color or prevent cars from being that color.
- make everything independent from the tick frequency. (cars' speed shouldn't be influenced by it, for example.)
- fix the import mess. move imports to the top of source files. initialize all modules in an intialization function; not on import. (this should probably include not using curses' wrapper function anymore. Use exception handling to restore the terminal to a sane state when an error occurs instead.)
- after making the changes above, make sure that the error message that can result from a failure at loading the keyboard module (and other error messages generated through sys.exit) is still visible. (if we have our own exception handler around main now, does it need to print the string contents of the exceptions it catches?)
- in this readme file, describe everything the user should know about running the game as the root user and how that affects controls if you're on Linux. (see comments in the input module and in the documentation of the keyboard module itself.)
- module attributes that shouldn't be visible from other modules should have a name beginning with an underscore, as per PEP 8.
- make sure all the cool parts of the original Cope with Cops are here. (Including explosions and stuff.)
- make sure the thing works on most PCs. (Make sure it works on Windows too. Also make sure smooth steering − through the keyboard module − is always used there, since it doesn't require administrative privileges there.)
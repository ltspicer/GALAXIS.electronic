# GALAXIS.electronic
Ravensburger game from 1980
I coded the Ravensburger game "GALAXIS electronic" from 1980 for fun and as a Python exercise.

Installation:

Windows users must install Python 3.7 or higher (see https://bodo-schoenfeld.de/installation-von-python-unter-windows-10/ ). Reboot after installation!
Python3.x should already be pre-installed in Linux systems. However, ev pip3 has to be installed afterwards (sudo apt install pip3).

Unzip the zip and start galaxy.py in the resulting directory.
Missing libraries should be installed automatically on first start.
In some cases you have to restart the game up to 2 times when you start it for the first time so that the libraries that have just been installed are taken over.


Game Instructions:

Offline (1 player):
There have been 4 starships lost in the galaxy.
It is important to find them.
Right-click on a point in the coordinate system.
Searching for spaceships. Namely horizontally, vertically and diagonally.
The number of detected spaceships is then displayed on this dot.
Spaceships behind a spaceship are of course not recognized.
Points where no spaceship can be can be marked in black with the left mouse button.
Clicking on it again removes the marking.
For example, with a 0 there are definitely no more spaceships to be found in all 8 directions from this point. These points can be marked in black.
The game is over when all 4 spaceships have been found.

Online (2 players):
To start the network game, simply enter your nickname after galaxy.py. Eg ./galaxy.py daniel
Now you have to hide your 4 spaceships, which your opponent has to find.
You have 60 seconds to think and aim. Otherwise the opponent gets a turn.
Available opponents in the network are displayed in the console, in which a chat is also running.
Enter 'gegner={nickname}' to connect to an opponent. Now the "found" sound is played to alert both players.
In rare cases, the message "Your opponent has disappeared from the network. Please restart." appears.
This happens when your opponent unexpectedly abandoned the game.
Then you have to restart the game and hide the spaceships again.
The console also serves as a chat.

The starter.sh is the starter for Linux users. Adjust path! 
Other suggestions and bug reports are welcome.

Have fun
Daniel

PS:
The exe is for Windows users without install Python.
Start with: starter.bat

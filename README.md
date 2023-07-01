# GALAXIS.electronic

Ravensburger game from 1980

---------------------

Read the file Anleitung.txt

Lies die Datei Anleitung.txt

---------------------

Game Instructions:

Offline (1 player) starts if NO nickname is entered:

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

PS:
The high score is 9 moves. If you beat them, take a screenshot and post it here:
https://www.ltspiceusers.ch/threads/ravensburger-galaxis-electronic-1980-f%C3%BCr-pc-off-online.989/#post-2643

Online (2 players) starts when a nickname is entered (at least 3 characters):

Now you have to hide your 4 spaceships (clicking on it again removes the spaceship), which your opponent has to find.
Select an opponent by entering their nickname in the text field below.
After the first move you have 60 seconds to think and aim. Otherwise the opponent gets a turn.
Available opponents in the network are displayed. A chat is running on the right side. Here you can enter messages, which will then be sent to all players present.
Enter your text with the keyboard and confirm with ENTER.
Now the "found" sound is played to alert both players.
In rare cases, the message "Your opponent has disappeared from the network. Please restart." appears.
This happens when your opponent unexpectedly abandoned the game.
Then you have to restart the game and hide the spaceships again.

You can also play against the server. This opponent is called "robot" ! So enter "opponent=robot" in the chat.
The roboteasy is a bit easier to defeat.

------------------

Spiel Anleitung:

Offline (1 Spieler) startet, wenn KEIN Nickname eingegeben wird:

Es sind 4 Raumschiffe in der Galaxis verloren gegangen.
Diese gilt es zu finden.
Mit rechter Maustaste auf einen Punkt im Koordinatensystem klicken.
Es wird nach Raumschiffen gesucht. Und zwar horizontal, vertikal und diagonal.
Die Anzahl erkannter Raumschiffe wird dann auf diesem Punkt angezeigt.
Raumschiffe hinter einem Raumschiff werden natürlich nicht erkannt.
Mit der linken Maustaste können Punkte, in welchen kein Raumschiff sein kann, schwarz markiert werden.
Erneuter Klick darauf entfernt die Markierung wieder.
ZBsp bei einer 0 sind in allen 8 Richtungen von diesem Punkt aus sicher keine Raumschiffe mehr zufinden. Diese Punkte können schwarz markiert werden.
Das Spiel ist fertig, wenn alle 4 Raumschiffe gefunden wurden.

PS:
Die Hi-Score ist 9 Spielzüge. Falls Du diese unterbietest, mach doch einen Screenshot davon und poste den unter:
https://www.ltspiceusers.ch/threads/ravensburger-galaxis-electronic-1980-f%C3%BCr-pc-off-online.989/#post-2643

Online (2 Spieler) startet, wenn ein Nickname eingegeben wird (mind. 3 Zeichen):

Nun musst Du Deine 4 Raumschiffe verstecken (erneuter Klick darauf entfernt das Raumschiff wieder), welche Dein Gegner zufinden hat.
Wähle einen Gegner aus, indem Du dessen Nickname ins Textfeld unten eingibst.
Nach dem ersten Zug hast Du jeweils 60 Sekunden Zeit zum überlegen und anpeilen. Sonst kommt der Gegner zum Zug.
Verfügbare Gegner im Netz werden angezeigt. Auf der rechten Seite läuft ein Chat. Hier kannst Du Nachrichten eingeben, welche dann an alle anwesenden Spieler gesendet werden.
Gib dazu Deinen Text mit der Tastatur ein und bestätige mit ENTER.
Nun wird der "gefunden" Sound abgespielt, um beide Spieler aufmerksam zu machen.
In seltenen Fällen kann es vorkommen, dass die Meldung "Dein Gegner ist aus dem Netzwerk verschwunden. Bitte neu starten." erscheint.
Das geschieht, wenn dein Gegner das Spiel unvorhergesehen abgebrochen hat.
Dann musst Du das Spiel neu starten und die Raumschiffe nochmal verstecken.

Du kannst auch gegen den Server spielen. Dieser Gegner heisst "robot" ! Gib also "gegner=robot" im Chat ein.
Der roboteasy ist etwas einfacher zu besiegen.

---------------------

Required files/directories for the Windows exe:
- **data** directory
- **config.ini** file
- **updater.bat** file
- **galaxis.exe** file

Required files/directories for the Python3 variant:
- **data** directory
- **config.ini** file
- **updater.bat** file
- **updater.sh** file
- **galaxis.py** file
- **PodSixNet** directory (only for Python 3.12+ needed)

Required files/directories for the Linux binary:
- **data** directory
- **config.ini** file
- **updater.sh** file
- **galaxis** file

On Raspberry (Raspbian/Raspi-OS) works the Python3 variant fine.

The PodSixNet directory is necessary for Python 3.12 or higher.
Just copy this into the game directory (parallel to galaxis.py & data Directory).

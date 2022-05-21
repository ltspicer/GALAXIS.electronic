# GALAXIS.electronic

Ravensburger game from 1980

---------------------

English translator version:


I coded the Ravensburger game "GALAXIS electronic" from 1980 for fun and as a Python exercise.

Installation:

Windows users must install Python 3.7 or higher (see https://bodo-schoenfeld.de/installation-von-python-unter-windows-10/ ). Reboot after installation!
Python3.x should already be pre-installed in Linux systems. However, ev pip3 has to be installed afterwards (sudo apt install python3-pip).

Unzip the zip and start galaxy.py in the resulting directory (Linux users have to select "run in terminal").
Missing libraries should be installed automatically on first start.

Alternative for Windows users: Click galaxis.exe (no Python needed). However, the config file is not read there. Therefore a galaxy_en.exe is available.

In Linux, if no "run in terminal" option is available or a starter is created, run starter.sh.

You can adjust the language in the file config.py (language = "en").

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

Now you have to hide your 4 spaceships (right mouse button), which your opponent has to find.
After the first move you have 60 seconds to think and aim. Otherwise the opponent gets a turn.
Available opponents in the network are displayed in the console, in which a chat is also running. Here you can enter messages, which will then be sent to all players present.
Enter 'opponent={nickname}' to connect to an opponent (eg opponent=daniel ). Now the "found" sound is played to alert both players.
In rare cases, the message "Your opponent has disappeared from the network. Please restart." appears.
This happens when your opponent unexpectedly abandoned the game.
Then you have to restart the game and hide the spaceships again.


Other suggestions and bug reports are welcome.

Have fun
Daniel


Home of this game: https://www.ltspiceusers.ch/threads/galaxis-electronic-1980-von-ravensburger-python3-spiel.989/#post-2643

----------------------------------------

Original Text deutsch:

Habe aus Spass und zur Python-Übung das Ravensburger Spiel "GALAXIS electronic" von 1980 gecodet.

Installation:

Windows-User müssen Python 3.7 oder höher installieren (siehe https://bodo-schoenfeld.de/installation-von-python-unter-windows-10/ ). Nach der Installation einen Reboot machen!
In Linux Systemen sollte Python3.x bereits vorinstalliert sein. Allerdings muss da ev pip3 nachinstalliert werden ( sudo apt install python3-pip ).
Und tkinter ( sudo apt-get install -y python3-tk ).

Zip entpacken und galaxis.py im entstandenen Verzeichnis starten (in Linux "im Terminal ausführen" auswählen).
Fehlende Bibliotheken sollten beim Erststart automatisch installiert werden.

Alternative für Windows Benutzer: Klicke galaxis.exe (keine Python Installation notwendig).
Allerdings wird da die config Datei nicht gelesen. Darum eine galaxis_en.exe verfügbar.

In Linux, wenn keine Option "im Terminal ausführen" zur Verfügung steht oder ein Starter angelegt wird, starter.sh ausführen.

Die Sprache kann in der Datei config.py eingestellt werden (language = "de").


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

Nun musst Du Deine 4 Raumschiffe verstecken (rechte Maustaste), welche Dein Gegner zufinden hat.
Nach dem ersten Zug hast Du jeweils 60 Sekunden Zeit zum überlegen und anpeilen. Sonst kommt der Gegner zum Zug.
Verfügbare Gegner im Netz werden in der Konsole angezeigt, in welcher auch ein Chat läuft. Hier kannst Du Nachrichten eingeben, welche dann an alle anwesenden Spieler gesendet werden.
Gib 'gegner={nickname}' ein, um Dich mit einem Gegner zu verbinden (ZBsp  gegner=daniel  ). Nun wird der "gefunden" Sound abgespielt, um beide Spieler aufmerksam zu machen.
In seltenen Fällen kann es vorkommen, dass die Meldung "Dein Gegner ist aus dem Netzwerk verschwunden. Bitte neu starten." erscheint.
Das geschieht, wenn dein Gegner das Spiel unvorhergesehen abgebrochen hat.
Dann musst Du das Spiel neu starten und die Raumschiffe nochmal verstecken.


Weitere Anregungen und Bugreports sind willkommen.


Viel Spass

Daniel


Dieses Spiel ist hier zuhause: https://www.ltspiceusers.ch/threads/galaxis-electronic-1980-von-ravensburger-python3-spiel.989/#post-2643

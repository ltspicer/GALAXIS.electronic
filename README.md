# GALAXIS.electronic

Ravensburger game from 1980

---------------------


English translator version:


I coded the Ravensburger game "GALAXIS electronic" from 1980 for fun and as a Python exercise.

Installation:

Windows users must install Python 3.7 or higher (see https://bodo-schoenfeld.de/installation-von-python-unter-windows-10/ ). Reboot after installation!
Python3.x should already be pre-installed in Linux systems. However, ev pip3 has to be installed afterwards (sudo apt install python3-pip).
And tkinter ( sudo apt-get install -y python3-tk ).

Unzip the zip and start galaxy.py in the resulting directory.
Missing libraries should be installed automatically on first start.
In some cases you have to restart the game up to 3 times when you start it for the first time so that the libraries that have just been installed are taken over.


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

Online (2 players) starts when a nickname is entered (at least 3 characters):

Now you have to hide your 4 spaceships ('right mouse button', which your opponent has to find.
After the first move you have 60 seconds to think and aim. Otherwise the opponent gets a turn.
Available opponents in the network are displayed in the console, in which a chat is also running. Here you can enter messages, which will then be sent to all players present.
Enter 'gegner={nickname}' to connect to an opponent (eg gegner=daniel ). Now the "found" sound is played to alert both players.
In rare cases, the message "Dein Gegner ist aus dem Netzwerk verschwunden. Bitte neu starten." appears.
This happens when your opponent unexpectedly abandoned the game.
Then you have to restart the game and hide the spaceships again.


Other suggestions and bug reports are welcome.

Have fun
Daniel

PS:
The exe is for Windows users without install Python.
Start with double-click on galaxis.exe .

I found that Windows doesn't need the starter. Just click galaxis.exe!

Linux users can click the galaxy.py and select "run in terminal". The starter.sh is also superfluous here.

Home of this game: https://www.ltspiceusers.ch/threads/galaxis-electronic-1980-von-ravensburger-python3-spiel.989/#post-2643

----------------------------------------

Original Text deutsch:

Habe aus Spass und zur Python-Übung das Ravensburger Spiel "GALAXIS electronic" von 1980 gecodet.

Installation:

Windows-User müssen Python 3.7 oder höher installieren (siehe https://bodo-schoenfeld.de/installation-von-python-unter-windows-10/ ). Nach der Installation einen Reboot machen!
In Linux Systemen sollte Python3.x bereits vorinstalliert sein. Allerdings muss da ev pip3 nachinstalliert werden (sudo apt install python3-pip).
Und tkinter ( sudo apt-get install -y python3-tk ).

Zip entpacken und galaxis.py im entstandenen Verzeichnis starten.
Fehlende Bibliotheken sollten beim Erststart automatisch installiert werden.
In manchen Fällen muss man das Spiel beim Erststart bis zu 3 mal neu starten, damit die gerade installierten Libraries übernommen werden.


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

Online (2 Spieler) startet, wenn ein Nickname eingegeben wird (mind. 3 Zeichen):

Nun musst Du Deine 4 Raumschiffe verstecken, welche Dein Gegner zufinden hat.
Nach dem ersten Zug hast Du jeweils 60 Sekunden Zeit zum überlegen und anpeilen. Sonst kommt der Gegner zum Zug.
Verfügbare Gegner im Netz werden in der Konsole angezeigt, in welcher auch ein Chat läuft. Hier kannst Du Nachrichten eingeben, welche dann an alle anwesenden Spieler gesendet werden.
Gib 'gegner={nickname}' ein, um Dich mit einem Gegner zu verbinden (ZBsp  gegner=daniel  ). Nun wird der "gefunden" Sound abgespielt, um beide Spieler aufmerksam zu machen.
In seltenen Fällen kann es vorkommen, dass die Meldung "Dein Gegner ist aus dem Netzwerk verschwunden. Bitte neu starten." erscheint.
Das geschieht, wenn dein Gegner das Spiel unvorhergesehen abgebrochen hat.
Dann musst Du das Spiel neu starten und die Raumschiffe nochmal verstecken.


Weitere Anregungen und Bugreports sind willkommen.


Viel Spass

Daniel


PS:
Die exe ist für Windows User ohne Python Installation.
Starten mit Doppelklick auf galaxis.exe .

Habe festgestellt, dass unter Windows der Starter nicht notwendig ist. Einfach nur galaxis.exe anklicken!

Linux User können die galaxis.py anklicken und "im Terminal ausführen" wählen. So ist die starter.sh auch hier überflüssig.

Dieses Spiel ist hier zuhause: https://www.ltspiceusers.ch/threads/galaxis-electronic-1980-von-ravensburger-python3-spiel.989/#post-2643

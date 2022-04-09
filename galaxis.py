#!/usr/bin/python3

###############################
#  GALAXIS electronic V2.2    #
#  von Daniel Luginbuehl      #
#        (C) 2022             #
# webmaster@ltspiceusers.ch   #
#                             #
#        Serveradresse        #
#    galaxis.game-host.org    #
###############################

#### !! Aufruf mit Nickname = Netzwerk Spiel !! Bsp ./galaxis.py daniel

from __future__ import print_function

# network client

HOST_ADDR = "galaxis.game-host.org"   # Hier IP des Servers
HOST_PORT = 10002                     # Hier Port des Servers

try:
    import pygame
except ImportError as e:
    print("pygame ist nicht installiert, wird installiert!")
    import subprocess, sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pygame'])
    print("Pygame ist installiert. Starte mich neu!")
    sys.exit()

try:
    import PodSixNet
except ImportError as e:
    print("PodSixNet ist nicht installiert, wird installiert!")
    import subprocess, sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PodSixNet'])
    print("PodSixNet ist installiert. Starte mich neu!")
    sys.exit()

# Importieren der Bibliotheken
import sys, pygame, time, random, math, json, threading, socket
from pygame.locals import *
pygame.init()
from pygame import mixer
from sys import stdin
from time import sleep
from sys import stdin, exit


# Offline oder Netzwerk Spiel
try:
    n = sys.argv[1]
except IndexError:
    spielmodus = 1
else:
    spielmodus = 2
    nickname = n

#### Definitionen ####

# Korrekturfaktor berechnen
def kor(zahl):
    zahl = zahl * MULTIPLIKATOR
    return zahl

# Punkt zeichnen
def element_zeichnen(spalte,reihe,farbe):
    pygame.draw.ellipse(fenster, farbe, [kor(spalte)*4+2*MULTIPLIKATOR, kor(reihe)*4+2*MULTIPLIKATOR,kor(1),kor(1)], 0)

# Wert im Punkt zeichnen
def element_wert(spalte,reihe,wert):
    img = font.render(str(wert), True, SCHWARZ)
    fenster.blit(img, ([kor(spalte)*4+2.25*MULTIPLIKATOR, kor(reihe)*4+2.05*MULTIPLIKATOR]))

# Spielzüge zeichnen
def spielzuge(wert):
    stand = "Spielzüge: " + str(wert)
    imag = font.render(stand, True, BLAU)
    pygame.draw.rect(fenster, SCHWARZ, [kor(4.53)*4+2.66*MULTIPLIKATOR, kor(5.46)*4+2.17*MULTIPLIKATOR,kor(1.4),kor(1)], 0)
    fenster.blit(imag, ([kor(3.4)*4+2.25*MULTIPLIKATOR, kor(5.5)*4+2.05*MULTIPLIKATOR]))

# Spiel gewonnen
def gewonnen():
    imag = font.render("Spiel gewonnen. ESC zum Verlassen.", True, ROT)
    fenster.blit(imag, ([kor(2.0)*4+2.25*MULTIPLIKATOR, kor(3.5)*4+2.05*MULTIPLIKATOR]))

# Spiel verloren
def verloren(gegner_name):
    imag = font.render("Spiel verloren. ESC zum Verlassen.", True, ROT)
    fenster.blit(imag, ([kor(2.0)*4+2.25*MULTIPLIKATOR, kor(3.5)*4+2.05*MULTIPLIKATOR]))
    print("Gegner hat gewonnen!!!")
    #time.sleep(6.7)
    info = "Dein Gegner " + gegner_name + " hat gewonnen."
    userinfo(info)
    pygame.display.flip()
    mixer.music.load("gewonnen.mp3")
    mixer.music.play()


# Raumschiff zeichnen
def raumschiff_zeichnen(spalte,reihe,farbe):
    pygame.draw.ellipse(fenster, farbe, [kor(spalte)*4+1.5*MULTIPLIKATOR, kor(reihe)*4+1.5*MULTIPLIKATOR,kor(2),kor(2)], 0)

# Anfrage auswerten > return 5 = Raumschiff gefunden
def ping(spalte, reihe):
    mixer.music.load("suchen.mp3")
    mixer.music.play()
    time.sleep(3.6)
    n = 0
    if galaxis[reihe][spalte] == 5:
        if gefunden == 3:
            return 5
        mixer.music.load("gefunden.mp3")
        mixer.music.play()
        time.sleep(3.5)
        return 5
    # x-
    x = spalte
    while x > 0:
        x = x - 1
        if galaxis[reihe][x] == 5:
            n = n + 1
            break
    # x+
    x = spalte
    while x < 8:
        x = x + 1
        if galaxis[reihe][x] == 5:
            n = n + 1
            break
    # y-
    y = reihe
    while y > 0:
        y = y - 1
        if galaxis[y][spalte] == 5:
            n = n + 1
            break
    # y+
    y = reihe
    while y < 6:
        y = y + 1
        if galaxis[y][spalte] == 5:
            n = n + 1
            break
    # x- y-
    x = spalte
    y = reihe
    while x > 0 and y > 0:
        x = x - 1
        y = y - 1
        if galaxis[y][x] == 5:
            n = n + 1
            break
    # x+ y+
    x = spalte
    y = reihe
    while x < 8 and y < 6:
        x = x + 1
        y = y + 1
        if galaxis[y][x] == 5:
            n = n + 1
            break
    # x+ y-
    x = spalte
    y = reihe
    while x < 8 and y > 0:
        x = x + 1
        y = y - 1
        if galaxis[y][x] == 5:
            n = n + 1
            break
    # x- y+
    x = spalte
    y = reihe
    while x > 0 and y < 6:
        x = x - 1
        y = y + 1
        if galaxis[y][x] == 5:
            n = n + 1
            break
    if n==1:
        mixer.music.load("1beep.mp3")
        mixer.music.play()
        time.sleep(0.8)
    if n==2:
        mixer.music.load("2beep.mp3")
        mixer.music.play()
        time.sleep(1.4)
    if n==3:
        mixer.music.load("3beep.mp3")
        mixer.music.play()
        time.sleep(2.7)
    if n==4:
        mixer.music.load("4beep.mp3")
        mixer.music.play()
        time.sleep(2.7)
    if n==0:
        mixer.music.load("0beep.mp3")
        mixer.music.play()
        time.sleep(2.0)
    galaxis[reihe][spalte] = n
    return n

# Mauszeiger-Position berechnen
def fensterposition(x,y):
    x = abs((x - 0.6 * MULTIPLIKATOR)/(4 * MULTIPLIKATOR))
    y = abs((y - 0.6 * MULTIPLIKATOR)/(4 * MULTIPLIKATOR))
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    if x > 8:
        x = 8
    if y > 6:
        y = 6
    return x, y

def spielfeld_zeichnen():
    # Hintergrundbild holen
    bg = pygame.image.load("space5.jpg")

    # Hintergrundfarbe/Bild Fenster
    fenster.fill(SCHWARZ)
    fenster.blit(bg, (0, 0))

    # X Koordinaten zeichnen 1-9
    for x in range(0,9):
        img = font.render(str(x+1), True, WEISS)
        fenster.blit(img, (kor(x)*4+2.3*MULTIPLIKATOR, 12))

    # Y Koordinaten zeichnen A-G
    Ybuchstaben='GFEDCBA'
    for x in range(0,7):
        img = font.render(Ybuchstaben[x], True, WEISS)
        fenster.blit(img, (12, kor(x)*4+2.1*MULTIPLIKATOR))

    # Zeichnen der Punkte im Spielfenster
    for x in range(0,9):
        for y in range(0,7):
            element_zeichnen(x,y,GRAU)

# Sound initialisieren
mixer.init()
mixer.music.set_volume(0.7)

# Zeichensatz initialisieren
pygame.font.init()
font = pygame.font.SysFont(None, 27)

# Multiplikator
MULTIPLIKATOR = 20


# Bildschirm Aktualisierungen einstellen
clock = pygame.time.Clock()
pygame.key.set_repeat(10,0)

# genutzte Farben
GELB    = ( 255, 255,   0)
SCHWARZ = (   0,   0,   0)
GRAU    = ( 192, 192, 192)
ROT     = ( 255,   0,   0)
WEISS   = ( 255, 255, 255)
BLAU    = (  51, 255, 255)

# Spielfeld Vorgabewerte: 0-4 Rückgabewerte , 5 = Raumschiff , 6 = noch nicht angepeilt
galaxis=[
[6,6,6,6,6,6,6,6,6],
[6,6,6,6,6,6,6,6,6],
[6,6,6,6,6,6,6,6,6],
[6,6,6,6,6,6,6,6,6],
[6,6,6,6,6,6,6,6,6],
[6,6,6,6,6,6,6,6,6],
[6,6,6,6,6,6,6,6,6],
]

# Spielfeld: 1 = wenn bereits angepeilt , 0 = noch nicht angepeilt , 2 = schwarz markiert
angepeilt=[
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
]

if spielmodus == 1:

    # Spielfeld erzeugen über Berechnung
    fenster = pygame.display.set_mode((36 * MULTIPLIKATOR, 28 * MULTIPLIKATOR))

    # Titel für Fensterkopf
    pygame.display.set_caption("GALAXIS electronic")


    # Raumschiffe zufällig verstecken
    n=0
    while n<4:
        x = random.randint(0, 8)
        y = random.randint(0, 6)
        if galaxis[y][x] == 6:
            galaxis[y][x] = 5
            n=n+1

    spielfeld_zeichnen()

    gefunden = 0
    spielzuege = 0
    alarm = 0
    spielaktiv = True

    # Schleife Hauptprogramm
    while spielaktiv:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                spielaktiv = False
                #print("Spieler hat beendet")
                break


            if event.type == QUIT:
                pygame.quit()
                break
            elif event.type == MOUSEBUTTONDOWN:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                xpos, ypos = fensterposition(x,y)
                xpos = int(xpos)
                ypos = int(ypos)
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0] and angepeilt[ypos][xpos]==0:
                    element_zeichnen(xpos,ypos,SCHWARZ)
                    angepeilt[ypos][xpos] = 2
                elif mouse_presses[0] and angepeilt[ypos][xpos]==2:
                    element_zeichnen(xpos,ypos,GRAU)
                    angepeilt[ypos][xpos] = 0
                if mouse_presses[2] and angepeilt[ypos][xpos]==0:
                    spielzuege = spielzuege + 1
                    spielzuge(spielzuege)
                    wert = ping(xpos,ypos)
                    angepeilt[ypos][xpos] = 1
                    if wert==5:
                        raumschiff_zeichnen(xpos,ypos,ROT)
                        gefunden = gefunden + 1
                    else:
                        element_zeichnen(xpos,ypos,GELB)
                        element_wert(xpos,ypos,wert)

        # Fenster aktualisieren
        pygame.display.flip()

        # Refresh-Zeit festlegen
        clock.tick(100)

        if gefunden == 4 and alarm==0:
            alarm = 1
            gewonnen()
            pygame.display.flip()
            #print("Spiel gewonnen mit", spielzuege, "Spielzügen.")
            mixer.music.load("gewonnen.mp3")
            mixer.music.play()
            time.sleep(6.7)

    pygame.quit()
    sys.exit()


#### Netzwerk Spiel


import PodSixNet
from PodSixNet.Connection import connection, ConnectionListener
from _thread import *

# Anfrage auswerten

def netping(self, spalte, reihe, gefunden):   # Anfrage auswerten > return 5 = Raumschiff gefunden
    spalte = int(spalte)
    reihe = int(reihe)
    gefunden = int(gefunden)

    n = 0
    if self.galaxis[reihe][spalte] == 5:
        return 5
    # x-
    x = spalte
    while x > 0:
        x = x - 1
        if self.galaxis[reihe][x] == 5:
            n = n + 1
            break
    # x+
    x = spalte
    while x < 8:
        x = x + 1
        if self.galaxis[reihe][x] == 5:
            n = n + 1
            break
    # y-
    y = reihe
    while y > 0:
        y = y - 1
        if self.galaxis[y][spalte] == 5:
            n = n + 1
            break
    # y+
    y = reihe
    while y < 6:
        y = y + 1
        if self.galaxis[y][spalte] == 5:
            n = n + 1
            break
    # x- y-
    x = spalte
    y = reihe
    while x > 0 and y > 0:
        x = x - 1
        y = y - 1
        if self.galaxis[y][x] == 5:
            n = n + 1
            break
    # x+ y+
    x = spalte
    y = reihe
    while x < 8 and y < 6:
        x = x + 1
        y = y + 1
        if self.galaxis[y][x] == 5:
            n = n + 1
            break
    # x+ y-
    x = spalte
    y = reihe
    while x < 8 and y > 0:
        x = x + 1
        y = y - 1
        if self.galaxis[y][x] == 5:
            n = n + 1
            break
    # x- y+
    x = spalte
    y = reihe
    while x > 0 and y < 6:
        x = x - 1
        y = y + 1
        if self.galaxis[y][x] == 5:
            n = n + 1
            break

    return n

def sounds(n):
    if n==1:
        mixer.music.load("1beep.mp3")
        mixer.music.play()
        #time.sleep(0.8)
    if n==2:
        mixer.music.load("2beep.mp3")
        mixer.music.play()
        #time.sleep(1.4)
    if n==3:
        mixer.music.load("3beep.mp3")
        mixer.music.play()
        #time.sleep(2.7)
    if n==4:
        mixer.music.load("4beep.mp3")
        mixer.music.play()
        #time.sleep(2.7)
    if n==0:
        mixer.music.load("0beep.mp3")
        mixer.music.play()
        #time.sleep(2.0)
    #self.angepeilt[reihe][spalte] = 2

def sound_verraten():
    mixer.music.load("verraten.mp3")
    mixer.music.play()
    #time.sleep(6.6)

def sound_suchen():
    mixer.music.load('suchen.mp3')
    mixer.music.play()
    #time.sleep(3.4)

def sound_gefunden():
    mixer.music.load("gefunden.mp3")
    mixer.music.play()
    #time.sleep(3.5)

def sound_gewonnen():
    mixer.music.load("gewonnen.mp3")
    mixer.music.play()        

def userinfo(info):
    string = str(info)
    imag = font.render(string, True, BLAU)
    pygame.draw.rect(fenster, SCHWARZ, [kor(2.5)*1+0.00*MULTIPLIKATOR, kor(5.40)*5.4+0.07*MULTIPLIKATOR,kor(31.1),kor(1.2)], 0)
    fenster.blit(imag, ([kor(2.6)*1+0.00*MULTIPLIKATOR, kor(5.44)*5.4+0.00*MULTIPLIKATOR]))
    pygame.display.flip()



class GalaxisGame(ConnectionListener):

##### Warn-Timer #####

    def timer_starten(self):
        #print("timer_starten ausgeführt, threading.active_count()=", threading.active_count())
        if threading.active_count() == 1 and self.spielaktiv == True:
            self.timer = threading.Timer(54.0, self.timer54)
            self.timer.start()
            #print("timer54 gestartet")

    def timer_stoppen(self):
        #print("timer_stoppen, threading.active_count()=", threading.active_count())
        try:
            if self.timer.is_alive() == True:
                self.timer.cancel()
                self.umschalt_warnung = False
                #print("timer gestoppt")
        except:
            pass

    def timer54(self):
        self.timer_stoppen()
        self.timer = threading.Timer(6.0, self.timer6)
        if self.timer.is_alive() == False and self.spielaktiv == True:
            self.timer.start()
            # Hier Warnung auf Bildschirm
            self.umschalt_warnung = True
            print("noch 6 Sekunden!!!")

    def timer6(self):
        self.turn = False
        self.umschalt_warnung = False
        # Hier self.turn auf false setzen und an Gegner senden
        self.ping_remote(0, 0, 8, self.num, self.gameid)

##### Version abfragen

    def Network_version(self, data):
        version = data["version"]
        version = int(float(version) * 10)/10
        if version > self.version:
            print("Server Version:", version, " Client Version:", self.version)
            print("Bitte neue Spielversion verwenden.")
            print("Download: https://www.ltspiceusers.ch/threads/galaxis-electronic-1980-von-ravensburger-python3-spiel.989")
            connection.Close()
            pygame.quit()
            sleep(60)
            sys.exit()

##### Diverses für PodSixNet

    def Network_close(self, data):
        info = "Dein Gegner ist aus dem Netzwerk verschwunden. Bitte neu starten."
        userinfo(info)
        self.timer_stoppen()
        time.sleep(6)
        exit()

    def Network_players(self, data):
        string = [p for p in data['players'] if p != self.mein_name and p != "-"]
        if self.old_string != string:
            print("Verfügbare Spieler: " + ", ".join(string if len(string) > 0 else ["keine"]))
            self.old_string = string
    
    def Network_message(self, data):
        print(data['who'] + ": " + data['message'])

    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()

    def Network_connected(self, data):
        print("Du bist nun mit dem Server verbunden")
    
    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()

    def Network_num_gameid(self, data):
        #print("type data:", type(data))
        users = data["users"]
        self.num=data["player"]
        self.gameid=data["gameid"]
        self.userid=data["userid"]
        self.gegner=data["nickgegner"]
        gegner_bereit = data["bereit"]
        if len(list(filter(lambda x: self.mein_name in x, users))) > 0 and users != "-":
            print("Dein gewählter Nickname ist bereits vergeben!")
            self.mein_name = self.mein_name + str(self.userid)
            print("Dein neuer Nickname ist", self.mein_name)

        if gegner_bereit == True and self.spielerbereit == True:
            self.spielaktiv = True
            self.running = True
        if self.num == 0:
            self.turn = True
        else:
            self.turn = False
        if gegner_bereit == True:
            print("Gameid:", self.gameid, ", Userid:", self.userid)
            print("Spieler 0 beginnt. Du bist Spieler", self.num)

        connection.Send({"action": "nickname", "nickname": self.mein_name, "num": self.num, "gameid": self.gameid, "userid": self.userid})

    def Network_startgame(self, data):
        anzahl_spieler=data["players"]
        gameid=data["gameid"]
        bereit=data["bereit"]
        num=data["num"]
        gegnerbereit = False

        print("anzahl_spieler empfangen:", anzahl_spieler, "num:", num, "bereit:", bereit, "gegnerbereit:", gegnerbereit, "self.spielerbereit:", self.spielerbereit)
        if anzahl_spieler == 2 and gameid == self.gameid and self.spielerbereit == True:
            self.spielaktiv = True
            self.running = True
            if self.num != 0:
                self.turn = False
                self.ping_remote(0, 0, 8, self.num, self.gameid)   # Sag dem Gegner, dass er am Zug ist.
            print("mein_name:", self.mein_name, "gegner:", self.gegner)

##### Spielbezogene Funktionen

    def wer_ist_am_zug(self):
        if self.turn==True:
            info = self.mein_name + ", Du bist am Zug. Dein Gegner: " + str(self.gegner)
            userinfo(info)
        else:
            info = self.mein_name + ", dein Gegner " + str(self.gegner) + " ist am Zug"
            userinfo(info)

        if self.turn == True and self.spielzuege > 0:
            self.timer_starten()

    def mein_name_retour(self):
        return self.mein_name

    def ping_remote(self, xpos, ypos, wert, num, gameid):
        if self.galaxis[ypos][xpos] == 5:
            self.verraten = True
            raumschiff_zeichnen(xpos,ypos,SCHWARZ)
        else:
            self.verraten = False
        self.Send({"action": "antwort", "xpos": xpos, "ypos": ypos, "verraten": self.verraten, "num": num, "gameid": gameid, "gefunden": self.gefunden, "wert": wert})

    def Network_antwort(self, data):
        xpos = data["xpos"]
        ypos = data["ypos"]
        verraten = data["verraten"]
        num = data["num"]
        wert = data["wert"]
        gefunden = data["gefunden"]
        gameid = data["gameid"]
        #print("'antwort' von Server erhalten. x=", xpos, " y=", ypos, " verraten=", verraten, " von Spieler (num)", num, " gameid=", gameid, " gefunden=", gefunden, " wert=", wert)
        if num != self.num and wert == 8:  #### Gegner sagt, dass Du am Zug bist
            self.turn = True
            return

        if num != self.num and wert == 7: #### Gegner sagt, unternimm nichts
            return

        if num != self.num and wert == 6:  #### Anfrage von Gegner
            gesehn = netping(self, xpos, ypos, gefunden)
            #print("Anfrage von Gegner > netping xpos=", xpos, "ypos=", ypos, "gefunden=", gefunden)
            
            self.angepeilt[ypos][xpos] = 1
            if galaxis[ypos][xpos] == 6:
                element_zeichnen(xpos,ypos,SCHWARZ)
                self.turn = True
            if gesehn == 5:
                gefunden+=1
                self.turn = False
                raumschiff_zeichnen(xpos,ypos,SCHWARZ)  # Raumschiff aus galaxis Array löschen

            if gesehn < 5 and verraten == False:
                sounds(gesehn)
                self.turn = True
                #time.sleep(1)

            if gesehn == 5 and verraten == False:
                sound_gefunden()
                self.turn = False

            if gesehn == 5 and gefunden == 4:   # Gegner hat gewonnen!!!
                self.alarm = 1
                self.antwort = 10
                self.empfangen = True
                self.timer_stoppen()
                verloren(self.gegner)

            if verraten == True:
                self.gefunden+=1
                raumschiff_zeichnen(xpos,ypos,ROT)
                self.angepeilt[ypos][xpos] = 1
                if gefunden < 4 and self.gefunden == 4:
                    self.alarm = 1
                    self.antwort = 9
                    self.empfangen = True
                    self.timer_stoppen()
                    gewonnen()
                    sound_gewonnen()
                    info = "Du hast gegen " + str(self.gegner) + " gewonnen."
                    userinfo(info)
                    #time.sleep(5)
                    gesehn = 10

                elif gefunden == 4:   # Gegner hat gewonnen!!!
                    self.alarm = 1
                    self.antwort = 10
                    self.empfangen = True
                    self.timer_stoppen()
                    verloren(self.gegner)
                else:
                    time.sleep(2.9)
                    sound_verraten()

            self.ping_remote(xpos, ypos, gesehn, self.num, gameid) # Antwort an Gegner senden

        else:  #### Antwort von Gegner
            self.xpos = xpos
            self.ypos = ypos
            self.turn = False
            if wert == 10:
                self.timer_stoppen()
                verloren(self.gegner)
            if wert == 5:
                self.gefunden+=1
                self.turn = True
            if wert == 5 and self.gefunden == 4:   # Du hast gewonnen!!!
                self.timer_stoppen()
                print("Du hast gewonnen!!!")
            self.antwort = wert
            self.empfangen = True

    def __init__(self, mein_name):
        self.mein_name = mein_name

        # Spielfeld Vorgabewerte: 0-4 Rückgabewerte , 5 = Raumschiff , 6 = noch nicht angepeilt
        self.galaxis=[
        [6,6,6,6,6,6,6,6,6],
        [6,6,6,6,6,6,6,6,6],
        [6,6,6,6,6,6,6,6,6],
        [6,6,6,6,6,6,6,6,6],
        [6,6,6,6,6,6,6,6,6],
        [6,6,6,6,6,6,6,6,6],
        [6,6,6,6,6,6,6,6,6],
        ]

        # Spielfeld: 1 = wenn bereits angepeilt , 0 = noch nicht angepeilt , 2 = schwarz markiert
        self.angepeilt=[
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        ]


        self.players = []
        self.xpos = []
        self.ypos = []
        self.verraten = False
        self.wert = 6
        self.gefunden = 0
        self.antwort = 0
        self.spielerbereit = False
        self.gegner = "---"
        self.version = 2.2                  #### Hier die Client-Version!!!!
        self.spielaktiv = False
        self.old_string = ""

        #3
        #initialize pygame clock
        self.clock=pygame.time.Clock()

        if len(self.mein_name) < 3:
            print("Gib Deinen Nicknamen ein: ")
            while 1:
                self.mein_name = stdin.readline().rstrip("\n")
                if len(self.mein_name) > 2:
                    break
                print("Du musst Deinen Namen eingeben")


        #self.initSound()
        self.turn = False
        self.owner=[[0 for x in range(6)] for y in range(6)]
        self.me=0
        self.otherplayer=0
        self.didiwin=False
        self.running=False

        try:
            self.Connect((HOST_ADDR, HOST_PORT))

        except:
            print("Error Connecting to Server")
            exit()
        print("Galaxis Client gestartet")
        #connection.Send({"action": "nickname", "nickname": self.mein_name, "num": 0})

    def Galaxis(self):

        self.Send({"action": "spieler_bereit", "num": self.num, "gameid": self.gameid, "userid": self.userid, "bereit": self.spielerbereit})
        i = 0
        while not self.running:
            self.Pump()
            connection.Pump()
            sleep(1.5)
            i+=1
            if i == 40:
                i = 0
                self.ping_remote(0, 0, 7, self.num, self.gameid)   # Sag dem Gegner, dass er nichts machen soll. Timeout verhindern
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.spielaktiv = False
                    pygame.quit()
                    print("Spieler hat beendet")

                if event.type == QUIT:
                    pygame.quit()
                    self.spielaktiv = False


        sound_gefunden()
        self.spielzuege = 0
        self.alarm = 0
        self.umschalt_warnung = False

        # Schleife Hauptprogramm
        while self.spielaktiv:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.spielaktiv = False
                    #print("Spieler hat beendet")
                    self.timer_stoppen()
                    return self.spielaktiv

                if event.type == QUIT:
                    self.timer_stoppen()
                    pygame.quit()
                    self.spielaktiv = False
                    return self.spielaktiv

                elif event.type == MOUSEBUTTONDOWN:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    xpos, ypos = fensterposition(x,y)
                    xpos = int(xpos)
                    ypos = int(ypos)
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0] and self.angepeilt[ypos][xpos]==0:
                        element_zeichnen(xpos,ypos,SCHWARZ)
                        self.angepeilt[ypos][xpos] = 2
                    elif mouse_presses[0] and self.angepeilt[ypos][xpos]==2:
                        element_zeichnen(xpos,ypos,GRAU)
                        self.angepeilt[ypos][xpos] = 0
                    if mouse_presses[2] and self.angepeilt[ypos][xpos]==0 and self.turn == True:
                        self.timer_stoppen()
                        self.spielzuege+=1
                        sound_suchen()
                        self.empfangen = False
                        self.ping_remote(xpos,ypos, 6, self.num, self.gameid)
                        self.angepeilt[ypos][xpos] = 1
                        self.timer_stoppen()
                        while self.empfangen == False:
                            self.Pump()
                            connection.Pump()
                            sleep(0.01)
                        if self.antwort==10:
                            self.alarm = 1
                            self.timer_stoppen()
                            verloren(self.gegner)

                        if self.antwort==5:
                            raumschiff_zeichnen(xpos,ypos,ROT)
                            self.turn = True
                            time.sleep(3.8)
                            sound_gefunden()
                        elif self.antwort < 5:
                            element_zeichnen(xpos,ypos,GELB)
                            element_wert(xpos,ypos,self.antwort)
                            self.turn = False
                            time.sleep(3.8)
                            sounds(self.antwort)
                        else:
                            raumschiff_zeichnen(xpos,ypos,SCHWARZ)

                        if self.antwort==9:
                            self.gefunden = 4
                            self.antwort = 5
                            self.alarm = 0
                            self.timer_stoppen()
                            gewonnen()
                            info = "Du hast gegen " + str(self.gegner) + " gewonnen."
                            sound_gewonnen()
                            userinfo(info)

                        if self.verraten == True:
                            time.sleep(3.7)
                            sound_verraten()

                        #time.sleep(4.9)

            self.Pump()
            connection.Pump()
            sleep(0.01)

            # Fenster aktualisieren
            pygame.display.flip()

            # Refresh-Zeit festlegen
            clock.tick(100)

            if self.gefunden == 4 and self.alarm==0:
                self.alarm = 1
                gewonnen()
                self.timer_stoppen()
                info = "Du hast gegen " + str(self.gegner) + " gewonnen."
                userinfo(info)
                pygame.display.flip()
                mixer.music.load("gewonnen.mp3")
                mixer.music.play()
                #time.sleep(6.7)

            # Ausgabe, wer am Zug ist
            elif self.spielaktiv == True:
                if self.umschalt_warnung == False:
                    self.wer_ist_am_zug()

                else:
                    info = "Noch 6 Sekunden, dann ist "+self.gegner+" am Zug!"
                    userinfo(info)

        return True


    def InputLoop(self):
        # horrid threaded input loop
        # continually reads from stdin and sends whatever is typed to the server

        while 1:
            # Wenn user eingabe, dann self.chat = False
            #connection.Send({"action": "gegnerauswahl", "gegner": stdin.readline().rstrip("\n"), "spieler": self.mein_name})
            input = stdin.readline().rstrip("\n")
#            if input == "exit":
#                pygame.quit()
#                sys.exit()
#                self.chat = False
#                return
            connection.Send({"action": "message", "message": input, "gameid": self.gameid, "user": self.mein_name})
            self.input = input
            self.Pump()
            connection.Pump()
            sleep(0.1)

    def update(self):
        #sleep to make the game 60 fps
        self.clock.tick(60)
        connection.Pump()
        self.Pump()

        for event in pygame.event.get():
            #quit if the quit button was pressed
            if event.type == pygame.QUIT:
                exit()
     
    def Loop(self):
        connection.Pump()
        self.Pump()

    def finished(self):
        self.screen.blit(self.gameover if not self.didiwin else self.winningscreen, (0,0))
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            pygame.display.flip()

##### Raumschiffe verstecken

    def Verstecken(self):
        anzahl_versteckt = 0
        i = 0
        while anzahl_versteckt < 4:
            i+=1
            if i == 7000:
                i = 0
                self.ping_remote(0, 0, 7, self.num, self.gameid)   # Sag dem Gegner, dass er nichts machen soll. Timeout verhindern
                connection.Pump()
                self.Pump()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.spielaktiv = False
                    print("Spieler hat beendet")
                    return self.spielaktiv
                if event.type == QUIT:
                    pygame.quit()
                    self.spielaktiv = False
                    return self.spielaktiv
                elif event.type == MOUSEBUTTONDOWN:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    xpos, ypos = fensterposition(x,y)
                    xpos = int(xpos)
                    ypos = int(ypos)
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[2] and self.galaxis[ypos][xpos]==6:
                        raumschiff_zeichnen(xpos,ypos,WEISS)
                        self.galaxis[ypos][xpos] = 5
                        anzahl_versteckt+=1

                    elif mouse_presses[2] or mouse_presses[0] and self.galaxis[ypos][xpos]==5:
                        raumschiff_zeichnen(xpos,ypos,GRAU)
                        self.galaxis[ypos][xpos] = 6
                        anzahl_versteckt-=1
                connection.Pump()
                self.Pump()

            # Fenster aktualisieren
            pygame.display.flip()

            # Refresh-Zeit festlegen
            clock.tick(100)

        info = self.mein_name+", warte auf Gegner"
        userinfo(info)

        self.spielerbereit = True

        return True


##### Chat Thread starten

    def Chat(self):
        self.chat = True
        self.input = ""

        t = start_new_thread(self.InputLoop, ())


##### Grundsätzliche Aufrufe

galax=GalaxisGame(nickname) #__init__ is called right here

if galax.Chat() == False:
    pygame.quit()
    sys.exit()

# Spielfeld erzeugen über Berechnung
fenster = pygame.display.set_mode((36 * MULTIPLIKATOR, 31 * MULTIPLIKATOR))

# Titel für Fensterkopf
pygame.display.set_caption("GALAXIS electronic")

spielfeld_zeichnen()

connection.Pump()
galax.Pump()

mein_name = str(galax.mein_name_retour())

# Raumschiffe verstecken

print("Wenn Du fertig versteckt hast, wähle mit 'gegner={nickname}' einen Gegner aus.")
print("ESC zum verlassen")

info = mein_name + ", verstecke Deine Raumschiffe (rechte Maustaste)"
userinfo(info)

if galax.Verstecken() == False:
    pygame.quit()
    sys.exit()

# Spiel starten

if galax.Galaxis() == False:
    pygame.quit()
    sys.exit()


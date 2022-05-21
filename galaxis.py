#!/usr/bin/python3

###############################
#  GALAXIS electronic V3.1    #
#  von Daniel Luginbuehl      #
#        (C) 2022             #
# webmaster@ltspiceusers.ch   #
#                             #
#        Serveradresse        #
#    galaxis.game-host.org    #
###############################


from __future__ import print_function
import os, sys, time, config
from time import sleep

# Netzwerk (Server)

HOST_ADDR = "galaxis.game-host.org"   # Hier IP des Servers
HOST_PORT = 10002                     # Hier Port des Servers
install = 0
language = config.language

# Import-Versuche

try:
    import pygame
except ImportError as e:
    print("pygame ist nicht installiert, wird installiert!")
    import subprocess, sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pygame'])
    install = 1
    print("Pygame ist installiert.")

try:
    import PodSixNet
except ImportError as e:
    print("PodSixNet ist nicht installiert, wird installiert!")
    import subprocess, sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PodSixNet'])
    install = 1
    print("PodSixNet ist installiert.")

try:
    import colorama
except ImportError as e:
    print("colorama ist nicht installiert, wird installiert!")
    import subprocess, sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'colorama'])
    install = 1
    print("colorama ist installiert.")

if install == 1:
    from colorama import Fore
    from colorama import Style
    print(Fore.RED + "Ich starte neu!" + Style.RESET_ALL)
    time.sleep(2)
    sys.stdout.flush()
    os.system('"' + sys.argv[0] + '"')
    sys.exit()
    quit()


# Importieren der Bibliotheken

import pygame as pg
import random, math, json, threading, socket
from pygame.locals import *
pygame.init()
from pygame import mixer
from sys import stdin, exit
from colorama import Fore
from colorama import Style
colorama.init()

# Pfad zu mp3 und jpg holen
pfad = os.path.dirname(os.path.abspath(__file__)) + os.sep + "data" + os.sep
#pfad = "data" + os.sep  # Für Windows exe (compilieren)

#### Definitionen ####

# GALAXIS Spielmodus Fenster
def user_eingabe():
    global spielmodus
    global nickname
    eingabe = (e2.get()).replace(" ", "") 
    #print("Eingabe:", eingabe)
    if len(eingabe) == 0:
        spielmodus = 1
        master.destroy()
        return
    if len(eingabe) > 2:
        spielmodus = 2
        nickname = eingabe
        master.destroy()
        return
    else:
        if language == "de":
            print("Gib Deinen Nicknamen ein (mind. 3 Zeichen)!")
        else:
            print("Enter your nickname (at least 3 characters)!")

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
    if language == "de":
        stand = "Spielzüge: " + str(wert)
    else:
        stand = "  Moves:      " + str(wert)
    imag = font.render(stand, True, BLAU)
    pygame.draw.rect(fenster, SCHWARZ, [kor(4.53)*4+2.66*MULTIPLIKATOR, kor(5.46)*4+2.17*MULTIPLIKATOR,kor(1.4),kor(1)], 0)
    fenster.blit(imag, ([kor(3.4)*4+2.25*MULTIPLIKATOR, kor(5.5)*4+2.05*MULTIPLIKATOR]))

# Spiel gewonnen
def gewonnen():
    if language == "de":
        imag = font.render("Spiel gewonnen :)", True, ROT)
    else:
        imag = font.render("Won the game :)", True, ROT)
    fenster.blit(imag, ([kor(2.0)*6+2.25*MULTIPLIKATOR, kor(3.5)*4+2.05*MULTIPLIKATOR]))

def gewonnen_offline():
    if language == "de":
        imag = font.render("Spiel gewonnen. ESC zum Verlassen.", True, ROT)
    else:
        imag = font.render("    Won the game. ESC to exit.", True, ROT)
    fenster.blit(imag, ([kor(2.0)*4+2.25*MULTIPLIKATOR, kor(3.5)*4+2.05*MULTIPLIKATOR]))

# Spiel verloren
def verloren(gegner_name):
    if language == "de":
        imag = font.render("Spiel verloren :(", True, ROT)
        fenster.blit(imag, ([kor(2.0)*6+2.25*MULTIPLIKATOR, kor(3.5)*4+2.05*MULTIPLIKATOR]))
        print("Gegner hat gewonnen!!!")
        #time.sleep(6.7)
        info = "Dein Gegner " + gegner_name + " hat gewonnen."
    else:
        imag = font.render("Lost the game :(", True, ROT)
        fenster.blit(imag, ([kor(2.0)*6+2.25*MULTIPLIKATOR, kor(3.5)*4+2.05*MULTIPLIKATOR]))
        print("Opponent won!!!")
        #time.sleep(6.7)
        info = "Your opponent " + gegner_name + " won."
    userinfo(info)
    pygame.display.flip()
    mixer.music.load(pfad + "gewonnen.mp3")
    mixer.music.play()

# Ja/Nein zeichnen
def ja_nein_zeichnen():
    if language == "de":
        imag = font.render("Möchtest Du noch eine Runde spielen?", True, ROT)
        fenster.blit(imag, ([kor(2.0)*4+1.90*MULTIPLIKATOR, kor(4.5)*4+2.05*MULTIPLIKATOR]))
        pygame.draw.ellipse(fenster, GELB, [kor(3)*4+1*MULTIPLIKATOR, kor(5.5)*4+1*MULTIPLIKATOR,kor(3),kor(3)], 0)
        pygame.draw.ellipse(fenster, GELB, [kor(5)*4+1*MULTIPLIKATOR, kor(5.5)*4+1*MULTIPLIKATOR,kor(3),kor(3)], 0)
        img = font.render(str("Ja"), True, SCHWARZ)
        fenster.blit(img, ([kor(3)*4+2.00*MULTIPLIKATOR, kor(5.5)*4+2.05*MULTIPLIKATOR]))
        img = font.render(str("Nein"), True, SCHWARZ)
        fenster.blit(img, ([kor(5)*4+1.50*MULTIPLIKATOR, kor(5.5)*4+2.05*MULTIPLIKATOR]))
    else:
        imag = font.render("Would you like to play another round?", True, ROT)
        fenster.blit(imag, ([kor(2.0)*4+1.90*MULTIPLIKATOR, kor(4.5)*4+2.05*MULTIPLIKATOR]))
        pygame.draw.ellipse(fenster, GELB, [kor(3)*4+1*MULTIPLIKATOR, kor(5.5)*4+1*MULTIPLIKATOR,kor(3),kor(3)], 0)
        pygame.draw.ellipse(fenster, GELB, [kor(5)*4+1*MULTIPLIKATOR, kor(5.5)*4+1*MULTIPLIKATOR,kor(3),kor(3)], 0)
        img = font.render(str("Yes"), True, SCHWARZ)
        fenster.blit(img, ([kor(3)*4+1.75*MULTIPLIKATOR, kor(5.5)*4+2.05*MULTIPLIKATOR]))
        img = font.render(str("No"), True, SCHWARZ)
        fenster.blit(img, ([kor(5)*4+2.00*MULTIPLIKATOR, kor(5.5)*4+2.05*MULTIPLIKATOR]))


# Raumschiff zeichnen
def raumschiff_zeichnen(spalte,reihe,farbe):
    pygame.draw.ellipse(fenster, farbe, [kor(spalte)*4+1.5*MULTIPLIKATOR, kor(reihe)*4+1.5*MULTIPLIKATOR,kor(2),kor(2)], 0)

# Anfrage auswerten > return 5 = Raumschiff gefunden
def ping(spalte, reihe):
    mixer.music.load(pfad + "suchen.mp3")
    mixer.music.play()
    time.sleep(3.6)
    n = 0
    if galaxis[reihe][spalte] == 5:
        if gefunden == 3:
            return 5
        mixer.music.load(pfad + "gefunden.mp3")
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
        mixer.music.load(pfad + "1beep.mp3")
        mixer.music.play()
        time.sleep(0.8)
    if n==2:
        mixer.music.load(pfad + "2beep.mp3")
        mixer.music.play()
        time.sleep(1.4)
    if n==3:
        mixer.music.load(pfad + "3beep.mp3")
        mixer.music.play()
        time.sleep(2.7)
    if n==4:
        mixer.music.load(pfad + "4beep.mp3")
        mixer.music.play()
        time.sleep(2.7)
    if n==0:
        mixer.music.load(pfad + "0beep.mp3")
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
    bg = pygame.image.load(pfad + "space5.jpg")

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

# Offline oder Netzwerk Spiel / Neu gestartet?


class InputBox:

    def __init__(self, x, y, w, h, text=""):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        if language == "de":
            self.beschreibung1 = FONT2.render("Für online Spiel, gib Deinen Nicknamen ein (mind 3 Buchstaben)", True, ROT)
            self.beschreibung2 = FONT2.render("Für offline Spiel, gib ENTER ein", True, ROT)
        else:
            self.beschreibung1 = FONT2.render("For online game, enter your nickname (at least 3 letters)", True, ROT)
            self.beschreibung2 = FONT2.render("For offline play, type ENTER", True, ROT)

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                #print(self.text)
                nickname = self.text
                return nickname
            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            # Re-render the text.
            self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

        screen.blit(self.beschreibung1, (25, 5))
        screen.blit(self.beschreibung2, (25, 31))


# genutzte Farben
GELB    = ( 255, 255,   0)
SCHWARZ = (   0,   0,   0)
GRAU    = ( 192, 192, 192)
ROT     = ( 255,   0,   0)
WEISS   = ( 255, 255, 255)
BLAU    = (  51, 255, 255)

restarted = False
nick = config.nick
try:
    nick = sys.argv[1]
except IndexError:
    pass

if nick == "-" or not nick.startswith("VorHanden-"):

    if len(nick) < 3:
        pg.init()
        screen = pg.display.set_mode((640, 150))
        if language == "de":
            pygame.display.set_caption("GALAXIS Spielmodus")
        else:
            pygame.display.set_caption("GALAXIS game mode")
        COLOR_INACTIVE = pg.Color('lightskyblue3')
        COLOR_ACTIVE = pg.Color('dodgerblue2')
        FONT = pg.font.Font(None, 32)
        FONT2 = pg.font.Font(None, 27)
        pygame.display.flip()
        clock = pg.time.Clock()
        input_box = InputBox(220, 100, 140, 32)
        done = False

        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                nickname = input_box.handle_event(event)
                if nickname != "-" and nickname != None:
                    #print(nickname)
                    if len(nickname) > 2:
                        spielmodus = 2
                        done = True
                    else:
                        spielmodus = 1
                        done = True
            input_box.update()
            screen.fill((30, 30, 30))
            input_box.draw(screen)
            pg.display.flip()
            clock.tick(30)
    else:
        nickname = nick
        spielmodus = config.spielmodus

else:
    nickname = nick.replace("VorHanden-", "")
    spielmodus = 2
    restarted = True


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
    if language == "de":
        pygame.display.set_caption("GALAXIS electronic   (ESC zum verlassen)")
    else:
        pygame.display.set_caption("GALAXIS electronic   (ESC to exit)")

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
            gewonnen_offline()
            pygame.display.flip()
            #print("Spiel gewonnen mit", spielzuege, "Spielzügen.")
            mixer.music.load(pfad + "gewonnen.mp3")
            mixer.music.play()
            time.sleep(6.7)

    pygame.quit()
    sys.exit()


#### Netzwerk Spiel

from PodSixNet.Connection import connection, ConnectionListener

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
        mixer.music.load(pfad + "1beep.mp3")
        mixer.music.play()
        #time.sleep(0.8)
    if n==2:
        mixer.music.load(pfad + "2beep.mp3")
        mixer.music.play()
        #time.sleep(1.4)
    if n==3:
        mixer.music.load(pfad + "3beep.mp3")
        mixer.music.play()
        #time.sleep(2.7)
    if n==4:
        mixer.music.load(pfad + "4beep.mp3")
        mixer.music.play()
        #time.sleep(2.7)
    if n==0:
        mixer.music.load(pfad + "0beep.mp3")
        mixer.music.play()
        #time.sleep(2.0)
    #self.angepeilt[reihe][spalte] = 2

def sound_verraten():
    mixer.music.load(pfad + "verraten.mp3")
    mixer.music.play()
    #time.sleep(6.6)

def sound_suchen():
    mixer.music.load(pfad + "suchen.mp3")
    mixer.music.play()
    #time.sleep(3.4)

def sound_gefunden():
    mixer.music.load(pfad + "gefunden.mp3")
    mixer.music.play()
    #time.sleep(3.5)

def sound_gewonnen():
    mixer.music.load(pfad + "gewonnen.mp3")
    mixer.music.play()

def sound_message():
    mixer.music.load(pfad + "message.mp3")
    mixer.music.play()
    #time.sleep(0.75)

def userinfo(info):
    farbe = BLAU
    string = str(info)
    if string.startswith("Noch 6 Sekunden") or string.startswith("6 seconds left"):
        farbe = ROT
        if language == "en":
            string = "6 seconds left"
    imag = font.render(string, True, farbe)
    pygame.draw.rect(fenster, SCHWARZ, [kor(2.5)*1+0.00*MULTIPLIKATOR, kor(5.40)*5.4+0.07*MULTIPLIKATOR,kor(31.1),kor(1.2)], 0)
    fenster.blit(imag, ([kor(2.6)*1+0.00*MULTIPLIKATOR, kor(5.44)*5.4+0.00*MULTIPLIKATOR]))
    pygame.display.flip()


##### Das Spiel


class GalaxisGame(ConnectionListener):

##### Warn-Timer #####

    def timer_starten(self):
#        print("timer_starten ausgeführt, threading.active_count()=", threading.active_count())
        if threading.active_count() < 3 and self.spielaktiv == True:
            self.timer = threading.Timer(54.0, self.timer54)
            self.timer.daemon = True
            self.timer.start()
#            print("timer_starten ausgeführt, threading.active_count()=", threading.active_count())


    def timer_stoppen(self):
        #print("timer_stoppen, threading.active_count()=", threading.active_count())
        try:
            if self.timer.is_alive() == True:
                self.timer.cancel()
                self.umschalt_warnung = False
#                print("timer gestoppt")
        except:
            pass

    def timer54(self):
        self.timer_stoppen()
        self.timer = threading.Timer(6.0, self.timer6)
        self.timer.daemon = True
        if self.timer.is_alive() == False and self.spielaktiv == True:
            self.timer.start()
            # Hier Warnung auf Bildschirm
            self.umschalt_warnung = True
            if language == "de":
                print("noch 6 Sekunden!!!")
            else:
                print("6 seconds left!!!")

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
            print(Fore.RED + "Server Version:", version, "/ Client Version:", self.version)
            if language == "de":
                print("Bitte neue Spielversion verwenden." + Style.RESET_ALL)
                print("Download bei")
                print(Fore.BLUE + Style.BRIGHT + "https://www.ltspiceusers.ch/threads/galaxis-electronic-1980-von-ravensburger-python3-spiel.989" + Style.RESET_ALL)
                print("oder")
                print(Fore.BLUE + Style.BRIGHT + "https://github.com/ltspicer/GALAXIS.electronic" + Style.RESET_ALL)
            else:
                print("Please use new game version." + Style.RESET_ALL)
                print("Download at")
                print(Fore.BLUE + Style.BRIGHT + "https://www.ltspiceusers.ch/threads/galaxis-electronic-1980-von-ravensburger-python3-spiel.989" + Style.RESET_ALL)
                print("or")
                print(Fore.BLUE + Style.BRIGHT + "https://github.com/ltspicer/GALAXIS.electronic" + Style.RESET_ALL)
            connection.Close()
            pygame.quit()
            sleep(15)
            sys.exit()

##### Diverses für PodSixNet

    def Network_close(self, data):
        if language == "de":
            info = "Dein Gegner ist aus dem Netzwerk verschwunden. Bitte neu starten."
        else:
            info = "Your opponent has disappeared from the network. Please restart."
        userinfo(info)
        self.timer_stoppen()
        time.sleep(1)
#        exit()
        self.spielaktiv = False
        self.spiel_fertig = False

    def Network_players(self, data):
        string = [p for p in data['players'] if p != self.mein_name and p != "-"]
        if self.old_string != string:
            if language == "de":
                print("Verfügbare Spieler: " + Fore.BLUE + Style.BRIGHT + ", ".join(string if len(string) > 0 else ["keine"])  + Style.RESET_ALL)
            else:
                print("Available players: " + Fore.BLUE + Style.BRIGHT + ", ".join(string if len(string) > 0 else ["none"])  + Style.RESET_ALL)
            self.old_string = string
            if self.running == False:
                sound_message()
    
    def Network_message(self, data):
        print(Fore.BLUE + Style.BRIGHT + data['who'] + ": " + data['message']  + Style.RESET_ALL)
        if self.running == False:
            sound_message()

    def Network_error(self, data):
        print('Fehler/error:', data['error'][1])
        connection.Close()

    def Network_connected(self, data):
        if language == "de":
            print("Du bist nun mit dem Server verbunden")
        else:
            print("You are now connected to the server")
    
    def Network_disconnected(self, data):
        if language == "de":
            print(Fore.RED + 'Sorry. Server nicht verbunden. Nach Spielneustart, Nachricht einfach nochmal eingeben!' + Style.RESET_ALL)
            exit()
        else:
            print(Fore.RED + 'Sorry server not connected. After a game restart, simply enter the message again!' + Style.RESET_ALL)
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
            if language == "de":
                print(Fore.RED + "Dein gewählter Nickname ist bereits vergeben!" + Style.RESET_ALL)
                self.mein_name = self.mein_name + str(self.userid)
                print(Fore.RED + "Dein neuer Nickname ist", self.mein_name + Style.RESET_ALL)
            else:
                print(Fore.RED + "Your chosen nickname is already taken!" + Style.RESET_ALL)
                self.mein_name = self.mein_name + str(self.userid)
                print(Fore.RED + "Your new nickname is", self.mein_name + Style.RESET_ALL)

        if gegner_bereit == True and self.spielerbereit == True:
            self.spielaktiv = True
            self.running = True
        if self.num == 0:
            self.turn = True
        else:
            self.turn = False
        if gegner_bereit == True:
            print("Gameid:", self.gameid, ", Userid:", self.userid)
            if language == "de":
                print("Spieler 0 beginnt. Du bist Spieler", self.num)
            else:
                print("Player 0 begins. You are player", self.num)

        connection.Send({"action": "nickname", "nickname": self.mein_name, "num": self.num, "gameid": self.gameid, "userid": self.userid})

    def Network_startgame(self, data):
        anzahl_spieler=data["players"]
        gameid=data["gameid"]
        bereit=data["bereit"]
        num=data["num"]
        gegnerbereit = False

        if language == "de":
            print("Anzahl Spieler empfangen:", anzahl_spieler, "Spieler:", num, "Bereit?", bereit, "Gegner bereit?", gegnerbereit, "Spieler bereit?", self.spielerbereit)
        else:
            print("Number of players received:", anzahl_spieler, "Player:", num, "Ready?", bereit, "Opponent ready?", gegnerbereit, "Player ready?", self.spielerbereit)
        if anzahl_spieler == 2 and gameid == self.gameid and self.spielerbereit == True:
            self.spielaktiv = True
            self.running = True
            if self.num != 0:
                self.turn = False
                self.ping_remote(0, 0, 8, self.num, self.gameid)   # Sag dem Gegner, dass er am Zug ist.
            if language == "de":
                print("Mein Name:", self.mein_name, "Gegner:", self.gegner)
            else:
                print("My name:", self.mein_name, "Opponent:", self.gegner)

##### Spielbezogene Funktionen

    def wer_ist_am_zug(self):
        if self.turn==True:
            if language == "de":
                info = self.mein_name + ", Du bist am Zug. Dein Gegner: " + str(self.gegner)
            else:
                info = self.mein_name + ", It's your turn. Your opponent: " + str(self.gegner)
        else:
            if language == "de":
                info = self.mein_name + ", dein Gegner " + str(self.gegner) + " ist am Zug"
            else:
                info = self.mein_name + ", it's your opponent's turn (" + str(self.gegner) + ")"

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

        if num != self.num and wert == 8:  #### Gegner sagt, dass Du am Zug bist
            self.turn = True
            return

        if num != self.num and wert == 7: #### Gegner sagt, unternimm nichts
            return

        if num != self.num and wert == 6:  #### Anfrage von Gegner
            gesehn = netping(self, xpos, ypos, gefunden)
            
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
                self.spiel_fertig = True
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
                    self.spiel_fertig = True
                    if language == "de":
                        info = "Du hast gegen " + str(self.gegner) + " gewonnen."
                    else:
                        info = "You won against " + str(self.gegner) + "."
                    userinfo(info)
                    #time.sleep(5)
                    gesehn = 10

                elif gefunden == 4:   # Gegner hat gewonnen!!!
                    self.alarm = 1
                    self.antwort = 10
                    self.empfangen = True
                    self.spiel_fertig = True
                    self.timer_stoppen()
                    verloren(self.gegner)
                else:
                    time.sleep(0.2)
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
                if language == "de":
                    print("Du hast gewonnen!!!")
                else:
                    print("You won!!!")
                self.spiel_fertig = True
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
        self.version = 3.1                  #### Hier die Client-Version!!!!
        self.spielaktiv = False
        self.old_string = ""
        self.spiel_fertig = False


        #initialize pygame clock
        self.clock=pygame.time.Clock()


        #self.initSound()
        self.turn = False
        self.owner=[[0 for x in range(6)] for y in range(6)]
        self.running=False

        try:
            self.Connect((HOST_ADDR, HOST_PORT))

        except:
            print("Serververbindung fehlgeschlagen! / Server connection failed!")
            time.sleep(5)
            sys.exit()
        print("Galaxis Client Version", self.version, "gestartet / started")


##### Die Game Klasse by self


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
                    if language == "de":
                        print("Spieler hat beendet")
                    else:
                        print("Player has finished")
                if event.type == QUIT:
                    pygame.quit()
                    self.spielaktiv = False


        sound_gefunden()
        self.spielzuege = 0
        self.alarm = 0
        self.umschalt_warnung = False

##### Game Hauptschleife
        while self.spielaktiv:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.spielaktiv = False
                    #print("Spieler hat beendet")
                    self.timer_stoppen()
                    self.spiel_fertig = True
                    return self.spiel_fertig

                if event.type == QUIT:
                    self.timer_stoppen()
                    pygame.quit()
                    self.spielaktiv = False
                    self.spiel_fertig = True
                    return self.spiel_fertig

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
                        self.angepeilt[ypos][xpos] = 1
                        sound_suchen()
                        time.sleep(3.4)
                        self.empfangen = False
                        self.ping_remote(xpos,ypos, 6, self.num, self.gameid)
                        self.timer_stoppen()
                        while self.empfangen == False:
                            self.Pump()
                            connection.Pump()
                            sleep(0.01)
                        if self.antwort==10:
                            self.alarm = 1
                            self.timer_stoppen()
                            verloren(self.gegner)
                            self.spiel_fertig = True

                        if self.antwort==5:
                            raumschiff_zeichnen(xpos,ypos,ROT)
                            self.turn = True
                            time.sleep(0.2)
                            sound_gefunden()
                        elif self.antwort < 5:
                            element_zeichnen(xpos,ypos,GELB)
                            element_wert(xpos,ypos,self.antwort)
                            self.turn = False
                            time.sleep(0.2)
                            sounds(self.antwort)
                        else:
                            raumschiff_zeichnen(xpos,ypos,SCHWARZ)

                        if self.antwort==9:
                            self.gefunden = 4
                            self.antwort = 5
                            self.alarm = 0
                            self.timer_stoppen()
                            gewonnen()
                            self.spiel_fertig = True
                            if language == "de":
                                info = "Du hast gegen " + str(self.gegner) + " gewonnen."
                            else:
                                info = "You won against " + str(self.gegner) + "."
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
                self.spiel_fertig = True
                if language == "de":
                    info = "Du hast gegen " + str(self.gegner) + " gewonnen."
                else:
                    info = "You won against " + str(self.gegner) + "."
                userinfo(info)
                pygame.display.flip()
                mixer.music.load(pfad + "gewonnen.mp3")
                mixer.music.play()
                #time.sleep(6.7)

            # Ausgabe, wer am Zug ist
            elif self.spielaktiv == True:
                if self.umschalt_warnung == False:
                    self.wer_ist_am_zug()
                else:
                    if language == "de":
                        info = "Noch 6 Sekunden, dann ist "+self.gegner+" am Zug!"
                    else:
                        info = "6 seconds left, then it's "+self.gegner+"'s turn!"
                    userinfo(info)

            if self.spiel_fertig == True:
                break

        return self.spiel_fertig

##### Der Terminal/Chat Thread

    def InputLoop(self):
        # horrid threaded input loop
        # continually reads from stdin and sends whatever is typed to the server
        while 1:
            input = stdin.readline().rstrip("\n")
            connection.Send({"action": "message", "message": input, "gameid": self.gameid, "user": self.mein_name})
            self.Pump()
            connection.Pump()
            sleep(0.1)


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
                    if language == "de":
                        print("Spieler hat beendet")
                    else:
                        print("Player has finished")
                    self.spiel_fertig = True
                    return self.spielaktiv
                if event.type == QUIT:
                    pygame.quit()
                    self.spielaktiv = False
                    self.spiel_fertig = True
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

        if language == "de":
            info = self.mein_name+", warte auf Gegner"
        else:
            info = self.mein_name+", wait for opponent"
        userinfo(info)

        self.spielerbereit = True

        return True


##### Chat Thread starten

    def Chat(self, restarted):
        self.restarted = restarted
#        self.input_thread = start_new_thread(self.InputLoop, ())
        input_thread = threading.Thread(target=self.InputLoop, name="input_thread")
        input_thread.daemon = True
        input_thread.start()
        self.input_thread = input_thread
        return self.input_thread


##### Grundsätzliche Aufrufe

galax=GalaxisGame(nickname) # __init__ wird hier aufgerufen

# Chat starten
input_thread = galax.Chat(restarted)

# Spielfeld erzeugen über Berechnung
fenster = pygame.display.set_mode((36 * MULTIPLIKATOR, 31 * MULTIPLIKATOR))

# Titel für Fensterkopf
if language == "de":
    pygame.display.set_caption("GALAXIS electronic   (ESC zum verlassen)")
else:
    pygame.display.set_caption("GALAXIS electronic   (ESC to exit)")

spielfeld_zeichnen()

connection.Pump()
galax.Pump()

mein_name = str(galax.mein_name_retour())

# Raumschiffe verstecken

if language == "de":
    print("Wenn Du fertig versteckt hast, wähle mit " + Fore.RED +"gegner={nickname}" + Style.RESET_ALL + " einen Gegner aus.")
    print("ESC im Spielfenster zum verlassen.")
    print("Gib hier Deine Chat-Nachrichten ein. Absenden mit ENTER")
    info = mein_name + ", verstecke Deine Raumschiffe (rechte Maustaste)"
else:
    print("When you have finished hiding, choose an opponent with " + Fore.RED + "opponent={nickname}" + Style.RESET_ALL)
    print("ESC in game window to exit.")
    print("Enter your chat messages here. Submit with ENTER")
    info = mein_name + ", hide your spaceships (right mouse button)"
userinfo(info)

if galax.Verstecken() == False:
    pygame.quit()
    sys.exit()

#### Spiel starten

if galax.Galaxis() == False:       # Spiel abgebrochen?
    if language == "de":
        print(Fore.RED + "Spiel abgebrochen" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Game aborted" + Style.RESET_ALL)

connection.Close()
#### Spiel neu starten?

ja_nein_zeichnen()

# Fenster aktualisieren
pygame.display.flip()

# Refresh-Zeit festlegen
clock.tick(100)

antwort_jn = "-"
while antwort_jn == "-":
    for event in pygame.event.get():
        pygame.display.flip()
        if event.type == MOUSEBUTTONDOWN:
            x = pygame.mouse.get_pos()[0]
            y = pygame.mouse.get_pos()[1]
            xpos, ypos = fensterposition(x,y)
            xpos = int(xpos)
            ypos = int(ypos)
            mouse_presses = pygame.mouse.get_pressed()
            if (mouse_presses[2] or mouse_presses[0]) and xpos == 3 and (ypos == 5 or ypos == 6):
                antwort_jn = "j"
                break
            if (mouse_presses[2] or mouse_presses[0]) and xpos == 5 and (ypos == 5 or ypos == 6):
                antwort_jn = "n"
                break

if antwort_jn == "j":
    pygame.display.quit()
    pygame.quit()
    sys.stdout.flush()
    os.system('"' + sys.argv[0] + '"' + str(" VorHanden-"+mein_name))
    sys.exit()
    quit()

else:
    pygame.quit()
    sys.exit()

#!/usr/bin/python3

###############################
#   GALAXIS electronic V7.4   #
#    von Daniel Luginbuehl    #
#         (C) 2022            #
#  webmaster@ltspiceusers.ch  #
#                             #
#        Serveradresse        #
#    galaxis.game-host.org    #
###############################


from __future__ import print_function
import os
import sys
import time
import configparser
import hashlib
import subprocess
import shutil
from time import sleep


#### Alles zur config.ini ####

# Bemerkungen für config.ini
REMARKS = """
# multiplikator = 20  --> entspricht einem Spielfeld von  720 x  560 Pixel / corresponds to a field of  720 x  560 pixels
# multiplikator = 30  --> entspricht einem Spielfeld von 1080 x  840 Pixel / corresponds to a field of 1080 x  840 pixels
# multiplikator = 40  --> entspricht einem Spielfeld von 1440 x 1120 Pixel / corresponds to a field of 1440 x 1120 pixels
# ...

# language = de  --> für deutsch / language = en  --> for english
# nick = -  --> Standard Start. nick = MyNickname  --> Startet die in spielmodus gewählte Variante mit diesem Nickname
#                                                      Starts the variant selected in 'spielmodus' with this nickname
# spielmodus = 1  --> offline | spielmodus = 2  --> online | Wenn nick ungleich '-'
#                                                          | If nick is not equal to '-'

#    Beispiel / Example:
#      nick = aaaa
#      spielmodus = 1

#    So startet das Spiel immer direkt in der offline Variante
#    So the game always starts directly in the offline version
"""

# config.ini schreiben
def write_config():
    config.set('DEFAULT', REMARKS, None)
    with open('config.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)

# config.ini vorhanden? Wenn nicht, dann erstellen
config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = str
if not os.path.isfile("config.ini"):
    config["DEFAULT"] = {"multiplikator": "25", "language": "de", "nick": "-", "spielmodus": "2", "hostaddr": "galaxis.game-host.org", "hostport": "10002", "local_hiscore": "0"}
    write_config()

# config.ini lesen
config.read("config.ini")
nick = config.get("DEFAULT", "nick")
language = config.get("DEFAULT", "language")
HOST_ADDR = config.get("DEFAULT", "hostaddr")
HOST_PORT = int(config.get("DEFAULT", "hostport"))
try:
    MULTIPLIKATOR = int(config.get("DEFAULT", "multiplikator"))
except configparser.Error:
    config.set("DEFAULT", "multiplikator", "25")
    MULTIPLIKATOR = int(25)
try:
    LOCAL_HISCORE = 63-int(int(config.get("DEFAULT", "local_hiscore"))**(1/2))
except configparser.Error:
    config.set("DEFAULT", "local_hiscore", "0")

write_config()

my_os=sys.platform      # Betriebssystem in my_os speichern
winexe = 0
if sys.argv[0].endswith("galaxis.exe") is True:     # wenn Windows exe
    winexe = 1
if sys.argv[0].endswith("galaxis") is True:         # wenn Linux bin
    winexe = 2

install = 0
restarted = False


#### Import-Versuche ####

if winexe == 0:

    def InstallFrage(wert):
        if install > 0:
            if language == "de":
                print("Ich kann versuchen, die fehlenden Pakete automatisch zu installieren.")
                print("q = Abbruch, o = Ok, automatisch installieren")
            else:
                print("I can try to install the missing packages automatically.")
                print("q = Abort, o = Ok, install automatically")
            antwort = input('[q/o]: ')
            if antwort == "q":
                return 2

            try:
                subprocess.check_call([sys.executable, '-m', 'pip', '-V'])
            except subprocess.CalledProcessError:
                print()
                if language == "de":
                    print("python3-pip ist nicht installiert!")
                    print("Installieren mit:")
                else:
                    print("python3-pip is not installed!")
                    print("Install with:")
                print()
                print("Debian/Ubuntu/Mint:    sudo apt install python3-pip")
                print("CentOS/Red Hat/Fedora: sudo dnf install --assumeyes python3-pip")
                print("MacOS:                 sudo easy_install pip")
                print("Windows:               https://www.geeksforgeeks.org/how-to-install-pip-on-windows/")
                print()

                if language == "de":
                    print("Fenster schliesst in 20 Sekunden.")
                else:
                    print("Window closes in 20 seconds.")

                sleep(20)
                return 2

            if wert-4 > -1:
                wert-=4
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'asynchat', '--break-system-packages'])
                except subprocess.CalledProcessError:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyasynchat', '--break-system-packages'])
                print("asynchat is installed / ist installiert")

            if wert-2 > -1:
                wert-=2
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PodSixNet', '--break-system-packages'])
                print("PodSixNet is installed / ist installiert")

            if wert-1 > -1:
                wert-=1
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pygame', '--break-system-packages'])

                print("Pygame is installed / ist installiert")

            return 1
        else:
            return 0

    try:
        import pygame
    except ImportError as e:
        if os.path.isdir(r"pygame"):
            shutil.rmtree("pygame")
        if os.path.isdir(r"pygame.libs"):
            shutil.rmtree("pygame.libs")
        if os.path.isdir(r"pygame-2.6.0.data"):
            shutil.rmtree("pygame-2.6.0.data")
        try:
            import pygame
        except ImportError as e:
            install+=1
            if language == "de":
                print("pygame ist nicht installiert!")
            else:
                print("pygame is not installed!")

    try:
        import PodSixNet
    except ImportError as e:
        install+=2
        if language == "de":
            print("PodSixNet ist nicht installiert!")
        else:
            print("PodSixNet is not installed!")

    try:
        import asynchat
    except ImportError as e:
        install+=4
        if language == "de":
            print("asynchat ist nicht installiert!")
        else:
            print("asynchat is not installed!")

    antwort = InstallFrage(install)
    if antwort == 2:
        sys.exit()
        quit()
    if antwort == 1:
        if language == "de":
            print("Ich starte neu!")
        else:
            print("I'm restarting!")
        time.sleep(2)
        sys.stdout.flush()
        os.system('"' + sys.argv[0] + '"')
        sys.exit()
        quit()
else:
    import pygame
    import PodSixNet

# Importieren der Bibliotheken

import pygame as pg
import random
import json
import threading
import socket
from pygame.locals import *
pygame.init()
from pygame import mixer
from sys import stdin
from re import sub
from ftplib import FTP, error_perm

print()

## Hintergrundbild zufällig bestimmen
bg_image = "space" + str(random.randint(1,9)) + ".jpg"

## Zeichensatz initialisieren
pygame.font.init()
font = pygame.font.SysFont(None, int(27 * MULTIPLIKATOR / 20))
font2 = pygame.font.SysFont(None, int(21 * MULTIPLIKATOR / 20))
font3 = pygame.font.SysFont(None, int(14 * MULTIPLIKATOR / 20))

# Pfad zu mp3 und jpg holen

if winexe == 0:
    pfad = os.path.dirname(os.path.abspath(__file__)) + os.sep + "data" + os.sep        # wenn Linux bin
else:
    pfad = "data" + os.sep                                                              # wenn Windows exe

#### Definitionen ####

# Alles für den Update

def move_all_files(src_dir, dest_dir):
    # Stelle sicher, dass das Quell- und Zielverzeichnis existieren
    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"Source directory {src_dir} does not exist.")
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Verschiebe alle Dateien und Verzeichnisse
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        try:
            # Wenn die Zieldatei oder das Zielverzeichnis existiert, entferne es
            if os.path.exists(dest_path):
                if os.path.isfile(dest_path):
                    os.remove(dest_path)
                elif os.path.isdir(dest_path):
                    shutil.rmtree(dest_path)
            
            # Jetzt verschiebe die Datei oder das Verzeichnis
            shutil.move(src_path, dest_dir)

        except Exception as e:
            print(f"Error moving {src_path} to {dest_path}: {e}")

def is_directory(ftp, name):
    """Überprüfe, ob ein Element ein Verzeichnis ist."""
    try:
        # Versuche, in das Verzeichnis zu wechseln
        ftp.cwd(name)
        ftp.cwd('..')  # Wechsel zurück zum vorherigen Verzeichnis
        return True
    except error_perm:
        return False

def download_ftp_directory(ftp, remote_dir, local_dir, win, unix, pyt, pygame_installed):
    # Erstelle das lokale Verzeichnis, falls es nicht existiert
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    # Wechsle in das Remote-Verzeichnis
    ftp.cwd(remote_dir)

    # Liste der Dateien und Verzeichnisse im Remote-Verzeichnis abrufen
    items = ftp.nlst()

    for item in items:
        local_path = os.path.join(local_dir, item)

        # Bedingung: Überspringe Verzeichnisse, die mit 'pygame' beginnen, falls compiled oder pygame_installed nicht vorhanden
        if item.startswith("pygame") and ((pyt and not pygame_installed) or not pyt):
            print(f"Skipping download of {item} while the game is compiled or pygame subdirectory is not present")
            continue

        # Bedingung: Überspringe Verzeichnisse, die mit 'async' beginnen, falls Python Variante nicht installiert
        if item.startswith("async") and not pyt:
            print(f"Skipping download of {item} while Python variant is not present")
            continue

        # Bedingung: Überspringe Verzeichnis 'PodSixNet', falls Python Variante nicht installiert
        if item == "PodSixNet" and not pyt:
            print("Skipping download of 'PodSixNet' while Python variant is not present")
            continue


        if is_directory(ftp, item):
            # Wenn es ein Verzeichnis ist, rekursiv herunterladen
            try:
                download_ftp_directory(ftp, item, local_path, win, unix, pyt, pygame_installed)
            except Exception as e:
                print(f"Error downloading directory {item}: {e}")
        else:
            # Überspringe den Download von 'galaxis.exe', wenn 'win' False ist
            if item == "galaxis.exe" and not win:
                print(f"Skipping download of {item} because Windows is {win}")
                continue
            # Überspringe den Download von 'galaxis', wenn 'unix' False ist
            if item == "galaxis" and not unix:
                print(f"Skipping download of {item} because Unix is {unix}")
                continue
            # Überspringe den Download von 'galaxis.py', wenn 'pyt' False ist
            if item == "galaxis.py" and not pyt:
                print(f"Skipping download of {item} because Python is {pyt}")
                continue
            # Wenn es eine Datei ist, herunterladen
            try:
                with open(local_path, 'wb') as f:
                    ftp.retrbinary('RETR ' + item, f.write)
                    print(f'Downloaded: {local_path}')
            except Exception as e:
                print(f'Error downloading {item}: {e}')

    # Wechsle zurück in das übergeordnete Verzeichnis
    try:
        ftp.cwd('..')  # Wechsel zurück zum vorherigen Verzeichnis
    except ftplib.error_perm as e:
        print(f'Error going back to parent directory: {e}')

def mainupdater(win, unix, pyt, pygame_installed):
    # FTP-Server-Daten
    HOST = 'galaxis.istmein.de'
    PORT = 4321  # Standard FTP-Port
    USER = 'galaxis'
    PASSWORD = 'electronic'
    REMOTE_DIR = 'source'  # Remote-Verzeichnis
    LOCAL_DIR = 'new_release'  # Lokales Verzeichnis

    # Verbinde mit dem FTP-Server
    ftp = FTP()
    ftp.connect(HOST, PORT)
    ftp.login(USER, PASSWORD)

    # Starte den Download des Remote-Verzeichnisses
    download_ftp_directory(ftp, REMOTE_DIR, LOCAL_DIR, win, unix, pyt, pygame_installed)

    # Verbindung schließen
    ftp.quit()

def updateme():
    # Exists Binary and/or Python file?
    unix, win, pyt = False, False, False
    unix1, win1, pyt1 = False, False, False
    if os.path.isfile("galaxis"):
        unix1 = True
    if os.path.isfile("galaxis.exe"):
        win1 = True
    if os.path.isfile("galaxis.py"):
        pyt1 = True

    if pyt1 and (win1 or unix1):
        if language == "de":
            print("Nebst der Python Variante ist auch installiert:")
        else:
            print("In addition to the Python variant is also installed:")
        print()
        if win1: print("Windows exe")
        if unix1: print("Linux Binary")
        print()
        if language == "de":
            print("Welche soll ich behalten?")
            print("A = Alle, L = nur Linux Binary,  W = nur Windows exe,  P = nur Python Variante, Q = Abbruch")
        else:
            print("Which ones should I keep?")
            print("A = All,  L = Linux binary only, W = Windows exe only, P = Python variant only, Q = Quit")
        print()
        
        while True:
            if language == "de":
                eingabe = "Wähle: "
            else:
                eingabe = "Select: "
            answer = input(eingabe).strip()
            if answer.lower().startswith('a'):
                if unix1: unix = True
                if win1: win = True
                if pyt1: pyt = True
                break
            if answer.lower().startswith('l') and unix1:
                unix = True
                break
            if answer.lower().startswith('w') and win1:
                win = True
                break
            if answer.lower().startswith('p') and pyt1:
                pyt = True
                break
            if answer.lower().startswith('q'):
                return
    else:
        unix = unix1
        win = win1
        pyt = pyt1

    # Exist pygame directory?
    pygame_installed = os.path.isdir("pygame")

    # Delete new_release directory
    shutil.rmtree("new_release", ignore_errors=True)

    # Download new release
    print()
    print("Starting download...")
    mainupdater(win, unix, pyt, pygame_installed)
    print("Download completed")
    print()

    # Remove directories in game root
    dirs_to_remove = ["data", "PodSixNet", "asyncore", "asynchat", "pygame", "pygame.libs", "pygame-2.6.0.data"]
    for f in dirs_to_remove:
        shutil.rmtree(f, ignore_errors=True)

    # Move all directories and files
    print("Move directories and files to game root")
    if winexe == 1:
        os.rename("new_release/galaxis.exe", "new_release/galaxis1.exe")
    move_all_files("new_release", ".")
#    if os.path.exists("config.ini"):
#        print("Backup config.ini")
#        shutil.move("config.ini", "new_release/config.ini")

    # Build starter.sh for Linux binary
    if unix:
        print("Build starter.sh")
    if unix and not pyt:
        with open("starter.sh", "w") as f:
            f.write("#!/bin/sh\n\n")
            f.write("export LD_PRELOAD=/usr/lib64/libstdc++.so.6\n")
            f.write("export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6\n\n")
            f.write('HOME="$(cd -- "$(dirname -- "$0")" && pwd)"\n')
            f.write('cd ${HOME} ; ./galaxis\n')

    if unix and pyt:
        with open("starter.sh", "w") as f:
            f.write("#!/bin/sh\n\n")
            f.write("export LD_PRELOAD=/usr/lib64/libstdc++.so.6\n")
            f.write("export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6\n\n")
            f.write('HOME="$(cd -- "$(dirname -- "$0")" && pwd)"\n')
            f.write('cd ${HOME} ; ./galaxis\n\n')
            f.write('#### starter for Python variant is different!!:\n\n')
            f.write('#HOME="$(cd -- "$(dirname -- "$0")" && pwd)"\n')
            f.write('#cd ${HOME} ; ./galaxis.py\n')

    # Remove excess files and directories
    print("Remove excess files and directories")
    if win and not unix:
        if os.path.exists("galaxis"):
            os.remove("galaxis")

    if win and not unix and not pyt:
        if os.path.exists("starter.sh"):
            os.remove("starter.sh")

    if unix and not win:
        if os.path.exists("galaxis.exe"):
            os.remove("galaxis.exe")

    if not pyt:
        shutil.rmtree("PodSixNet", ignore_errors=True)
        shutil.rmtree("asyncore", ignore_errors=True)
        shutil.rmtree("asynchat", ignore_errors=True)
        if os.path.exists("galaxis.py"):
            os.remove("galaxis.py")
        shutil.rmtree("pygame", ignore_errors=True)
        shutil.rmtree("pygame.libs", ignore_errors=True)
        shutil.rmtree("pygame-2.6.0.data", ignore_errors=True)
        # Make executable
        if unix and my_os != "win32":
            if os.path.exists("galaxis"):
                os.chmod("galaxis", 0o755)
        if win and my_os != "win32":
            if os.path.exists("galaxis.exe"):
                os.chmod("galaxis.exe", 0o755)
    elif pyt and my_os != "win32":
        if os.path.exists("galaxis.py"):
            os.chmod("galaxis.py", 0o755)

    # Make executable
    if os.path.exists("starter.sh") and my_os != "win32":
        os.chmod("starter.sh", 0o755)
    if os.path.exists("updater.py") and my_os != "win32":
        os.chmod("updater.py", 0o755)

    # Remove excess files
    if pyt and not unix:
        if os.path.exists("galaxis"):
            os.remove("galaxis")
    if pyt and not win:
        if os.path.exists("galaxis.exe"):
            os.remove("galaxis.exe")
    if os.path.exists("updater.bat"):
        os.remove("updater.bat")
    if os.path.exists("updater.sh"):
        os.remove("updater.sh")
    if os.path.exists("updater.py"):
        os.remove("updater.py")

    # Restore config.ini
#    if os.path.exists("new_release/config.ini"):
#        print("Restore config.ini")
#        shutil.move("new_release/config.ini", "config.ini")

    # Remove temp directory
    print("Remove temp directory")
    shutil.rmtree("new_release", ignore_errors=True)

    if winexe == 1:
        # Starte wincopier.exe
        try:
            subprocess.Popen(["wincopier.exe"])
            sys.exit()
        except Exception as e:
            print(f"Error when starting wincopier.exe: {e}")
            sys.exit(1)

    # Finish
    print()
    print("Info:")
    if language == "de":
        print("Wenn pip den Fehler 'externally-managed-environment' zurück gibt, siehe:")
    else:
        print("If pip returns the error 'externally-managed-environment', see:")
    print("https://www.makeuseof.com/fix-pip-error-externally-managed-environment-linux/")
    print()
    if language == "de":
        print("Bei grösseren Versionssprüngen (längere Zeit kein Update gemacht) kann es von Vorteil sein, den updater.py nochmal zu starten!")
    else:
        print("In the case of major version jumps (no update for a long time) it can be advantageous to start the updater.py again!")

# Weitere Funktionen für das Spiel

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
    pygame.draw.rect(fenster, SCHWARZ, [kor(4.45)*4+2.66*MULTIPLIKATOR, kor(5.46)*4+2.17*MULTIPLIKATOR,kor(1.8),kor(1)], 0)
    fenster.blit(imag, ([kor(3.4)*4+2.25*MULTIPLIKATOR, kor(5.5)*4+2.05*MULTIPLIKATOR]))

# Hiscore zeichnen
def hiscore():
    imag = font2.render("Hiscore: " + str(LOCAL_HISCORE), True, ROT)
    fenster.blit(imag, ([kor(0.4)*4+2.25*MULTIPLIKATOR, kor(5.5)*4+2.05*MULTIPLIKATOR]))

# Spiel gewonnen
def gewonnen():
    if language == "de":
        imag = font.render("Spiel gewonnen :)", True, ROT)
    else:
        imag = font.render("Won the game :)", True, ROT)
    fenster.blit(imag, ([kor(2.0)*6+2.25*MULTIPLIKATOR, kor(3.5)*4+2.05*MULTIPLIKATOR]))

def gewonnen_offline(info):
    imag = font.render(info, True, ROT)
    fenster.blit(imag, ([kor(1.0)*4+2.25*MULTIPLIKATOR, kor(3.5)*4+2.05*MULTIPLIKATOR]))

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
def ja_nein_zeichnen(grund):            # 0 noch eine Runde, 1 auto Update
    if language == "de":
        if grund == 0:
            imag = font.render("Möchtest Du noch eine Runde spielen?", True, ROT)
            fenster.blit(imag, ([kor(9.9), kor(20.05)]))
        else:
            imag = font.render("Neue Version verfügbar. Soll ich automatisch updaten?", True, ROT)
            fenster.blit(imag, ([kor(6.0), kor(20.05)]))
        pygame.draw.ellipse(fenster, GELB, [kor(3)*4+MULTIPLIKATOR, kor(5.5)*4+MULTIPLIKATOR,kor(3),kor(3)], 0)
        pygame.draw.ellipse(fenster, GELB, [kor(5)*4+MULTIPLIKATOR, kor(5.5)*4+MULTIPLIKATOR,kor(3),kor(3)], 0)
        img = font.render(str("Ja"), True, SCHWARZ)
        fenster.blit(img, ([kor(3)*4+2.00*MULTIPLIKATOR, kor(5.5)*4+2.05*MULTIPLIKATOR]))
        img = font.render(str("Nein"), True, SCHWARZ)
        fenster.blit(img, ([kor(5)*4+1.50*MULTIPLIKATOR, kor(5.5)*4+2.05*MULTIPLIKATOR]))
    else:
        if grund == 0:
            imag = font.render("Would you like to play another round?", True, ROT)
            fenster.blit(imag, ([kor(9.9), kor(20.05)]))
        else:
            imag = font.render("New version available. Should I update automatically?", True, ROT)
            fenster.blit(imag, ([kor(6.0), kor(20.05)]))
        pygame.draw.ellipse(fenster, GELB, [kor(3)*4+MULTIPLIKATOR, kor(5.5)*4+MULTIPLIKATOR,kor(3),kor(3)], 0)
        pygame.draw.ellipse(fenster, GELB, [kor(5)*4+MULTIPLIKATOR, kor(5.5)*4+MULTIPLIKATOR,kor(3),kor(3)], 0)
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

def chatfensterposition(x,y):
    x = abs((x - 0.6 * MULTIPLIKATOR)/(4 * MULTIPLIKATOR))
    y = abs((y - 0.6 * MULTIPLIKATOR)/(4 * MULTIPLIKATOR))
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    return x, y

# Spielfeld zeichnen
def spielfeld_zeichnen(bg_image):
    # Hintergrundbild holen
    bild = pygame.image.load(pfad + bg_image)
    bg = pygame.transform.scale(bild, (40 * MULTIPLIKATOR, 28 * MULTIPLIKATOR))

    # Hintergrundfarbe/Bild Fenster
    fenster.fill(SCHWARZ)
    fenster.blit(bg, (-50, 0))

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


# Offline oder Netzwerk Spiel und/oder Neu gestartet?

class InputBox:

    def __init__(self, x, y, w, h, text=""):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text+"_", True, self.color)
        self.active = False
        if language == "de":
            self.beschreibung1 = FONT2.render("Für online Spiel, gib Deinen Nicknamen ein (mind 3 Buchstaben)", True, ROT)
            self.beschreibung2 = FONT2.render("Für offline Spiel, ENTER drücken", True, ROT)
            self.beschreibung3 = FONT3.render("Für Update, #update eingeben", True, ROT)
        else:
            self.beschreibung1 = FONT2.render("For online game, enter your nickname (at least 3 letters)", True, ROT)
            self.beschreibung2 = FONT2.render("For offline game, press ENTER", True, ROT)
            self.beschreibung3 = FONT3.render("For Update, enter #update", True, ROT)

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                nickname = self.text
                return nickname
            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            # Re-render the text.
            self.txt_surface = FONT.render(self.text+"_", True, self.color)

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
        screen.blit(self.beschreibung3, (25, 59))


# genutzte Farben
GELB    = ( 255, 255,   0)
SCHWARZ = (   0,   0,   0)
GRAU    = ( 192, 192, 192)
ROT     = ( 255,   0,   0)
WEISS   = ( 255, 255, 255)
BLAU    = (  51, 255, 255)

# Nickname bearbeiten
def edit_nick(text=""):
    return sub('[^abcdefghijklmnopqrstuvwxyzäöüéèàABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ1234567890._]', '', text)

# Nickname bei Aufruf mitgegeben?
try:
    nick = sys.argv[1]
except IndexError:
    pass

nick = nick.replace(" ", "")

if nick == "-":
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
        FONT3 = pg.font.Font(None, 22)
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
                    nickname = nickname.replace(" ", "")
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
        spielmodus = int(config.get("DEFAULT", "spielmodus"))

else:
    nickname = nick
    if len(nickname) > 2:
        spielmodus = 2
    else:
        spielmodus = 1

if nickname == "#update":
    pygame.quit()
    updateme()
    print()
    if language == "de":
        print("Starte das Spiel neu.")
    else:
        print("Please restart the game.")
    sys.exit()
nickname = edit_nick(nickname)          # Nicht erlaubte Zeichen löschen
nickname = nickname[:10]                # Nickname auf 10 Zeichen kürzen

# Sound initialisieren
mixer.init()
mixer.music.set_volume(0.7)

# Multiplikator
#MULTIPLIKATOR = 20


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

if spielmodus == 1:         # Offline Spiel

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

    spielfeld_zeichnen(bg_image)
    hiscore()

    gefunden = 0
    spielzuege = 0
    alarm = 0
    spielaktiv = True

    # Spiel Hauptschleife
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
            mixer.music.load(pfad + "gewonnen.mp3")
            mixer.music.play()
            if LOCAL_HISCORE > spielzuege:
                if language == "en":
                    info = "          New hi-score! " + str(spielzuege) + " moves. ESC to exit."
                else:
                    info = "      Neue Hiscore! " + str(spielzuege) + " Spielzüge. ESC zum Verlassen."

                config['DEFAULT']['local_hiscore'] = str(int(63-spielzuege)**2)    # update
                write_config()
            else:
                if language == "en":
                    info = "       Game won with " + str(spielzuege) + " moves. ESC to exit."
                else:
                    info = "Spiel gewonnen mit " + str(spielzuege) + " Spielzügen. ESC zum Verlassen."
            gewonnen_offline(info)
            pygame.display.flip()
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
    pygame.draw.rect(fenster, SCHWARZ, [kor(2.5), kor(29.13),kor(34.8),kor(1.4)], 0)
    fenster.blit(imag, ([kor(2.6), kor(29.376)]))
    pygame.display.flip()

def md5(file1):
    md5h = hashlib.md5()
    with open(file1, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5h.update(chunk)
    return md5h.hexdigest()

def userinfotext(verfugbar, besetzt):
    farbe = BLAU
    verfugbar = ",".join(verfugbar)
    besetzt = ",".join(besetzt)
    if language == "de":
        verf = font2.render("Verfügbare Spieler: " + verfugbar, True, farbe)
        bese = font2.render("Besetzte Spieler: " + besetzt, True, farbe)
    else:
        verf = font2.render("Available players: " + verfugbar, True, farbe)
        bese = font2.render("Occupied players: " + besetzt, True, farbe)
    if verfugbar != "-":
        pygame.draw.rect(fenster, SCHWARZ, [kor(2.5), kor(30.7),kor(34),kor(1.2)], 0)
        fenster.blit(verf, ([kor(2.6)*1, kor(5.74)*5.4]))
    if besetzt != "-":
        pygame.draw.rect(fenster, SCHWARZ, [kor(2.5), kor(31.822),kor(34),kor(1.2)], 0)
        fenster.blit(bese, ([kor(2.6)*1, kor(5.92)*5.4]))
    pygame.display.flip()


##### Das Spiel

class GalaxisGame(ConnectionListener):

##### Warn-Timer #####

    def timer_starten(self):
        aktive_threads = threading.active_count()
        if aktive_threads < 2 and self.spielaktiv is True:
            self.timer = threading.Timer(54.0, self.timer54)
            self.timer.daemon = True
            self.timer.start()

    def timer_stoppen(self):
        try:
            if self.timer.is_alive() is True:
                self.timer.cancel()
                self.umschalt_warnung = False
        except:
            pass

    def timer54(self):
        self.timer_stoppen()
        self.timer = threading.Timer(6.0, self.timer6)
        self.timer.daemon = True
        if self.timer.is_alive() is False and self.spielaktiv is True:
            self.timer.start()
            # Hier Warnung auf Bildschirm
            self.umschalt_warnung = True
            if language == "de":
                print("noch 6 Sekunden!!!")
            else:
                print("6 seconds left!!!")

    def timer6(self):        # Hier self.turn auf false setzen und an Gegner senden
        self.turn = False
        self.umschalt_warnung = False
        self.ping_remote(0, 0, 8, self.num, self.gameid)

##### Version abfragen

    def Updater(self):
        pygame.quit()
        updateme()
        print()
        if language == "de":
            print("Starte das Spiel neu.")
        else:
            print("Please restart the game.")
        sys.exit()

    def Network_version(self, data):
        version = data["version"]
        version = int(float(version) * 10)/10
        if version > self.version:
            print("Server Version:", version, " / Client Version:", self.version)
            self.chatausgabe("Server Version: " + str(version) + "/ Client Version: " + str(self.version))
            if language == "de":
                print("Bitte neue Spielversion verwenden.")
                print("Download bei")
                print("https://www.ltspiceusers.ch/threads/galaxis-electronic-1980-von-ravensburger-python3-spiel.989")
                print("oder")
                print("https://github.com/ltspicer/GALAXIS.electronic")
                print("oder")
                print("https://ltspicer.itch.io/galaxis-electronic")
                print(" ")
                print("Soll ich automatisch updaten (j/n)?")
                self.chatausgabe("Bitte neue Spielversion verwenden.")
                self.chatausgabe("Download bei")
                self.chatausgabe(" ")
                self.chatausgabe("https://www.ltspiceusers.ch/threads/galaxis-elec")
                self.chatausgabe("  tronic-1980-von-ravensburger-python3-spiel.989")
                self.chatausgabe(" ")
                self.chatausgabe("oder")
                self.chatausgabe(" ")
                self.chatausgabe("https://github.com/ltspicer/GALAXIS.electronic")
                self.chatausgabe(" ")
                self.chatausgabe("oder")
                self.chatausgabe(" ")
                self.chatausgabe("https://ltspicer.itch.io/galaxis-electronic")
                self.chatausgabe(" ")
                self.chatausgabe("Soll ich automatisch updaten (j/n)?")
            else:
                print("Please use new game version.")
                print("Download at")
                print("https://www.ltspiceusers.ch/threads/galaxis-electronic-1980-von-ravensburger-python3-spiel.989")
                print("or")
                print("https://github.com/ltspicer/GALAXIS.electronic")
                print("or")
                print("https://ltspicer.itch.io/galaxis-electronic")
                print(" ")
                print("Should I update automatically (y/n)?")
                self.chatausgabe("Please use new game version.")
                self.chatausgabe("Download at")
                self.chatausgabe(" ")
                self.chatausgabe("https://www.ltspiceusers.ch/threads/galaxis-elec")
                self.chatausgabe("  tronic-1980-von-ravensburger-python3-spiel.989")
                self.chatausgabe(" ")
                self.chatausgabe("or")
                self.chatausgabe(" ")
                self.chatausgabe("https://github.com/ltspicer/GALAXIS.electronic")
                self.chatausgabe(" ")
                self.chatausgabe("or")
                self.chatausgabe(" ")
                self.chatausgabe("https://ltspicer.itch.io/galaxis-electronic")
                self.chatausgabe(" ")
                self.chatausgabe("Should I update automatically (y/n)?")
            connection.Close()
            ja_nein_zeichnen(1)
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
                self.Updater()
            pygame.quit()
            sys.exit()

        if winexe == 0:
            checksumme = md5("galaxis.py")
        if winexe == 1:
            checksumme = md5("galaxis.exe")
        if winexe == 2:
            checksumme = md5("galaxis")
        self.Send({"action": "checksumme", "summe": checksumme, "gameid": self.gameid, "userid": self.userid})


##### Diverses für PodSixNet

    def Network_checksum(self, data):
        status=data["status"]
        if status is False:
            if language == "de":
                print("Der Quellcode wurde verändert. Bitte aktuelle Version runterladen!")
                print("Download bei")
                print("https://www.ltspiceusers.ch/threads/galaxis-electronic-1980-von-ravensburger-python3-spiel.989")
                print("oder")
                print("https://github.com/ltspicer/GALAXIS.electronic")
                print("oder")
                print("https://ltspicer.itch.io/galaxis-electronic")
                print(" ")
                print("Soll ich sie automatisch holen (j/n)?")
                self.chatausgabe("Der Quellcode wurde verändert. Bitte aktuelle Version runterladen!")
                self.chatausgabe("Download bei")
                self.chatausgabe(" ")
                self.chatausgabe("https://www.ltspiceusers.ch/threads/galaxis-elec")
                self.chatausgabe("  tronic-1980-von-ravensburger-python3-spiel.989")
                self.chatausgabe(" ")
                self.chatausgabe("oder")
                self.chatausgabe(" ")
                self.chatausgabe("https://github.com/ltspicer/GALAXIS.electronic")
                self.chatausgabe(" ")
                self.chatausgabe("oder")
                self.chatausgabe(" ")
                self.chatausgabe("https://ltspicer.itch.io/galaxis-electronic")
                self.chatausgabe(" ")
                self.chatausgabe("Soll ich sie automatisch holen (j/n)?")
            else:
                print("The source code was modified manually. Please download current version!")
                print("Download at")
                print("https://www.ltspiceusers.ch/threads/galaxis-electronic-1980-von-ravensburger-python3-spiel.989")
                print("or")
                print("https://github.com/ltspicer/GALAXIS.electronic")
                print("or")
                print("https://ltspicer.itch.io/galaxis-electronic")
                print(" ")
                print("Should I fetch them automatically (y/n)?")
                self.chatausgabe("The source code was modified manually. Please download current version!")
                self.chatausgabe("Download at")
                self.chatausgabe(" ")
                self.chatausgabe("https://www.ltspiceusers.ch/threads/galaxis-elec")
                self.chatausgabe("  tronic-1980-von-ravensburger-python3-spiel.989")
                self.chatausgabe(" ")
                self.chatausgabe("or")
                self.chatausgabe(" ")
                self.chatausgabe("https://github.com/ltspicer/GALAXIS.electronic")
                self.chatausgabe(" ")
                self.chatausgabe("or")
                self.chatausgabe(" ")
                self.chatausgabe("https://ltspicer.itch.io/galaxis-electronic")
                self.chatausgabe(" ")
                self.chatausgabe("Should I fetch them automatically (y/n)?")
            connection.Close()
            ja_nein_zeichnen(1)
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
                self.Updater()
            pygame.quit()
            sys.exit()

    def Network_close(self, data):
        if language == "de":
            info = "Dein Gegner ist aus dem Netzwerk verschwunden. Bitte neu starten."
        else:
            info = "Your opponent has disappeared from the network. Please restart."
        userinfo(info)
        self.timer_stoppen()
        time.sleep(1)
#        sys.exit()
        self.spielaktiv = False
        self.spiel_fertig = False

    def Network_players(self, data):
        string = [p for p in data['players'] if p != self.mein_name and p != "-"]
        if self.old_string != string:
            userinfotext(string, "-")
            if language == "de":
                print("Verfügbare Spieler: " + ", ".join(string if len(string) > 0 else ["keine"]) )
            else:
                print("Available players: " + ", ".join(string if len(string) > 0 else ["none"]) )
            self.old_string = string
            if self.running == False:
                sound_message()

    def Network_busyplayers(self, data):
        string = [p for p in data['players'] if p != "-"]
        if self.old_string2 != string:
            userinfotext("-", string)
            if language == "de":
                print("Besetzte Spieler: " + ", ".join(string if len(string) > 0 else ["keine"]) )
            else:
                print("Occupied players: " + ", ".join(string if len(string) > 0 else ["none"]) )
            self.old_string2 = string
            if self.running == False:
                sound_message()

    def multiline_chatausgabe(self, text):      # Für Hiscore Ausgabe
        for message in text:
            self.chattext.append(message)
            print(message)
        while len(self.chattext) > 62:
            del self.chattext[0]
        pygame.draw.rect(fenster, SCHWARZ, [kor(37.4), kor(0.1),kor(18.9),kor(29.1)], 0)
        pygame.draw.rect(fenster, BLAU, [kor(37.5), kor(0.2),kor(18.3),kor(28.9)], 1)
        pygame.display.flip()
        zeile = 0
        for line in self.chattext:
            text = font3.render(line, True, BLAU)
            screen.blit(text, (kor(37.6), kor(0.3+zeile)))
            pygame.display.update()
            zeile+=0.46
        pygame.display.flip()

    def Network_message(self, data):
        # Hiscore Ausgabe?
        if data['who'] == "":
            if data['message'].startswith("---------------------------------------------"):
                if self.server_message_counter == 0:
                    self.server_messages = []
                self.server_message_counter+=1
        else:
            self.server_message_counter=0

        # Wenn nicht Hiscore Ausgabe
        if self.server_message_counter == 0:
            print(data['who'] + ": " + data['message'] )
            self.chatausgabe(data['who'] + ": " + data['message'])
            if self.running == False and data['who'] != "robot" and data['who'] != "roboteasy":
                sound_message()
            if (data["message"].startswith("Dein gewählter Gegner ist noch nicht bereit!") or data["message"].startswith("Your chosen opponent is not ready yet!")) and data["who"] == self.mein_name:
                self.gegner_verbunden = False

        # Wenn Hiscore Ausgabe, dann in self.server_messages speichern
        if self.server_message_counter > 0:
            self.server_messages.append(data['who'] + ": " + data['message'])

        # Wenn Hiscore Tabelle komplett, dann ausgeben
        if self.server_message_counter == 3:
            self.server_message_counter=0
            self.multiline_chatausgabe(self.server_messages)
            self.server_messages = []

    def Network_error(self, data):
        print('Fehler/error:', data['error'][1])
        connection.Close()

    def Network_connected(self, data):
        if language == "de":
            print("Du bist nun mit dem Server verbunden")
        else:
            print("You are now connected to the server")
        print()
    
    def Network_disconnected(self, data):
        if language == "de":
            print('Sorry. Server nicht verbunden.')
            sys.exit()
        else:
            print('Sorry server not connected.')
            sys.exit()

    def Network_num_gameid(self, data):
        #print("type data:", type(data))
        users = data["users"]
        self.num=data["player"]
        self.gameid=data["gameid"]
        self.userid=data["userid"]
        self.gegner=data["nickgegner"]
        self.gegner_bereit = data["bereit"]
        if self.mein_name == "robot" or self.mein_name == "roboteasy":
            if language == "de":
                print("Dieser Nickname ist nicht erlaubt!")
                self.chatausgabe("Dieser Nickname ist nicht erlaubt!")
            else:
                print("This nickname is not allowed!")
                self.chatausgabe("This nickname is not allowed!")
            time.sleep(8)
            pygame.display.quit()
            pygame.quit()
            sys.exit()
            quit()

        if len(list(filter(lambda x: self.mein_name in x, users))) > 0 and users != "-" and self.restarted is False:
            if language == "de":
                print("Dein gewählter Nickname ist bereits vergeben!")
                self.mein_name = self.mein_name + str(self.userid)
                print("Dein neuer Nickname ist", self.mein_name)
                self.chatausgabe("Dein gewählter Nickname ist bereits vergeben!")
                self.chatausgabe("Dein neuer Nickname ist " + self.mein_name)
            else:
                print("Your chosen nickname is already taken!")
                self.mein_name = self.mein_name + str(self.userid)
                print("Your new nickname is", self.mein_name)
                self.chatausgabe("Your chosen nickname is already taken!")
                self.chatausgabe("Your new nickname is " + self.mein_name)

        restarted = False
        if self.gegner_bereit and self.spielerbereit:
            self.spielaktiv = True
            self.running = True
        if self.num == 0:
            self.turn = True
        else:
            self.turn = False
        if self.gegner_bereit:
            print("Gameid:", self.gameid, ", Userid:", self.userid)
            if language == "de":
                print("Spieler 0 beginnt. Du bist Spieler", self.num)
                self.chatausgabe("Spieler 0 beginnt. Du bist Spieler " + str(self.num))
            else:
                print("Player 0 begins. You are player", self.num)
                self.chatausgabe("Player 0 begins. You are player " + str(self.num))

        connection.Send({"action": "nickname", "nickname": self.mein_name, "num": self.num, "gameid": self.gameid, "userid": self.userid, "sprache": language})

    def Network_startgame(self, data):
        anzahl_spieler=data["players"]
        gameid=data["gameid"]
        bereit=data["bereit"]
        num=data["num"]
        gegnerbereit = False

        if anzahl_spieler == 2 and gameid == self.gameid and self.spielerbereit:
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

    def raumschiff_loeschen(self):
        spielfeld_zeichnen(self.bg_image)
        for ypos in range(7):
            for xpos in range(9):
                if self.galaxis[ypos][xpos] == 5:
                    raumschiff_zeichnen(xpos,ypos,WEISS)

    def wer_ist_am_zug(self):
        if self.turn:
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

        if self.turn and self.spielzuege > 0:
            self.timer_starten()

    def mein_name_retour(self):
        return self.mein_name

    def ping_remote(self, xpos, ypos, wert, num, gameid):
        if self.galaxis[ypos][xpos] == 5:
            if gameid != -1:
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

        if num != self.num and wert == 7:  #### Gegner sagt, unternimm nichts
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

            if gesehn < 5 and verraten is False:
                sounds(gesehn)
                self.turn = True
                #time.sleep(1)

            if gesehn == 5 and verraten is False:
                sound_gefunden()
                self.turn = False

            if gesehn == 5 and gefunden == 4:   # Gegner hat gewonnen!!!
                self.alarm = 1
                self.antwort = 10
                self.empfangen = True
                self.spiel_fertig = True
                self.timer_stoppen()
                verloren(self.gegner)

            if verraten:
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

    def __init__(self, mein_name, bg_image):
        self.mein_name = mein_name
        self.restarted = False

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
        self.version = 7.40
        self.spielaktiv = False
        self.old_string = ""
        self.old_string2 = ""
        self.spiel_fertig = False

        self.bg_image = bg_image

        #initialize pygame clock
        self.clock=pygame.time.Clock()


        #self.initSound()
        self.turn = False
        self.running=False
        self.text = ""
        self.chattext = []

        try:
            self.Connect((HOST_ADDR, HOST_PORT))

        except:
            print("Serververbindung fehlgeschlagen! / Server connection failed!")
            time.sleep(5)
            sys.exit()
        print("Galaxis Client Version", self.version, "gestartet / started")

    def Neustart(self):
        self.restarted = True
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
        self.spielaktiv = False
        self.old_string = ""
        self.old_string2 = ""
        self.spiel_fertig = False

        # Hintergrundbild zufällig bestimmen
        self.bg_image = "space" + str(random.randint(1,9)) + ".jpg"

        #initialize pygame clock
        self.clock=pygame.time.Clock()

        #self.initSound()
        self.turn = False
        self.running=False
        self.text = ""

        try:
            self.Connect((HOST_ADDR, HOST_PORT))

        except:
            print("Serververbindung fehlgeschlagen! / Server connection failed!")
            time.sleep(5)
            sys.exit()
        return self.bg_image

    def Warten(self):       # 2 Sekunden warten, dabei "Gegner verbunden" Status abfragen
        i = 0
        while True:
            self.Pump()
            connection.Pump()
            time.sleep(0.01)
            i+=1
            if i == 200:
                return self.gegner_verbunden

    def chatausgabe(self, text):
        if text != "":
            self.chattext.append(text)
        if len(self.chattext) > 62:
            del self.chattext[0]
        pygame.draw.rect(fenster, SCHWARZ, [kor(37.4), kor(0.1),kor(18.9),kor(29.1)], 0)
        pygame.draw.rect(fenster, BLAU, [kor(37.5), kor(0.2),kor(18.3),kor(28.9)], 1)
        pygame.display.flip()
        zeile = 0
        for line in self.chattext:
            text = font3.render(line, True, BLAU)
            screen.blit(text, (kor(37.6), kor(0.3+zeile)))
            pygame.display.update()
            zeile+=0.46
        pygame.display.flip()

##### Spiel Hauptschleife
    def Galaxis(self):
        self.chatausgabe("")
        self.inputbox_zeichnen("", False)
        self.spielzuege = 0
        self.alarm = 0
        self.umschalt_warnung = False
        self.timer_stoppen()
        i = 0
        while not self.running:
            self.Pump()
            connection.Pump()
            sleep(0.01)
            i+=1
            if i == 6000:
                i = 0
                self.ping_remote(0, 0, 7, self.num, self.gameid)   # Sag dem Gegner, dass er nichts machen soll. Timeout verhindern
            pygame.display.flip()
        sound_gefunden()
        while self.spielaktiv:
            event1 = pygame.event.get()
            if len(event1) > 0:
                for event in event1:
                    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.spielaktiv = False
                        if language == "de":
                            print("Spieler hat beendet")
                        else:
                            print("Player has finished")
                        self.spiel_fertig = True
                        return self.spielaktiv

                    if event.type == pygame.KEYDOWN and event.type != QUIT:
                        self.chatinput(event.unicode[:1])

                    if event.type == QUIT:
                        pygame.quit()
                        self.spielaktiv = False
                        self.spiel_fertig = True
                        return self.spielaktiv
                    elif event.type == MOUSEBUTTONDOWN:
                        x = pygame.mouse.get_pos()[0]
                        y = pygame.mouse.get_pos()[1]
                        xpos, ypos = chatfensterposition(x,y)
                        xpos = int(xpos)
                        ypos = int(ypos)
                        mouse_presses = pygame.mouse.get_pressed()
                        if xpos < 9 and ypos < 7:
                            if mouse_presses[0] and self.angepeilt[ypos][xpos]==0:
                                element_zeichnen(xpos,ypos,SCHWARZ)
                                self.angepeilt[ypos][xpos] = 2
                            elif mouse_presses[0] and self.angepeilt[ypos][xpos]==2:
                                element_zeichnen(xpos,ypos,GRAU)
                                self.angepeilt[ypos][xpos] = 0
                            if mouse_presses[2] and self.angepeilt[ypos][xpos]==0 and self.turn:
                                self.turn = False
                                self.timer_stoppen()
                                self.spielzuege+=1
                                self.angepeilt[ypos][xpos] = 1
                                sound_suchen()
                                time.sleep(3.4)
                                self.empfangen = False
                                self.ping_remote(xpos,ypos, 6, self.num, self.gameid)
                                self.timer_stoppen()
                                while self.empfangen is False:
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

                                if self.verraten:
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
            elif self.spielaktiv:
                if self.umschalt_warnung is False:
                    self.wer_ist_am_zug()
                else:
                    if language == "de":
                        info = "Noch 6 Sekunden, dann ist "+self.gegner+" am Zug!"
                    else:
                        info = "6 seconds left, then it's "+self.gegner+"'s turn!"
                    userinfo(info)

            if self.spiel_fertig:
                self.spielaktiv = False

        return self.spiel_fertig

    def inputbox_zeichnen(self, text, gegner_auswahl):
        pygame.draw.rect(fenster, SCHWARZ, [kor(37.4), kor(29.25),kor(19.5),kor(2.9)], 0)
        pygame.draw.rect(fenster, BLAU, [kor(37.5), kor(29.25),kor(18.3),kor(1.1)], 1)
        pg.key.set_repeat()
        text_surf = font2.render(text+"_", True, BLAU)
        fenster.blit(text_surf, ([kor(37.6), kor(29.376)]))
        if gegner_auswahl is False:
            if language == "de":
                chatanleitung = "Chat Eingabe.              Senden mit ENTER"
            else:
                chatanleitung = "Chat input.                 Send with ENTER"
        else:
            if language == "de":
                chatanleitung = "Hier klicken um eine Chat-Nachricht einzugeben"
            else:
                chatanleitung = "Click here to enter a chat message"
        text_surf = font2.render(chatanleitung, True, BLAU)
        fenster.blit(text_surf, ([kor(37.9), kor(29.376+1.5)]))
        pygame.display.flip()


    def chatinput(self, text):
        self.inputbox_zeichnen(text, False)
        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[2] or mouse_presses[0]:
                    self.inputbox_zeichnen("", False)
                    return
                if event.type == pygame.QUIT:
                    run = False
                    text = ""
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_RETURN:
                        run = False
                    elif event.key == pygame.K_BACKSPACE:
                        text =  text[:-1]
                    else:
                        text += event.unicode[:1]
                    text_surf = font2.render(text+"_", True, BLAU)
                    pygame.draw.rect(fenster, SCHWARZ, [kor(37.6), kor(29.35),kor(17.7),kor(0.9)], 0)
                    fenster.blit(text_surf, ([kor(37.6), kor(29.376)]))
                connection.Pump()
                self.Pump()
                pygame.display.flip()
        connection.Send({"action": "message", "message": text, "gameid": self.gameid, "user": self.mein_name})
        self.Pump()
        connection.Pump()
        self.inputbox_zeichnen("", False)


##### Raumschiffe verstecken

    def Verstecken(self, info):
        self.spielerbereit = False
        anzahl_versteckt = 0
        i = 0
        verfugbar, besetzt = "-", "-"
        userinfotext(verfugbar, besetzt)
        self.chatausgabe("")
        self.inputbox_zeichnen("", False)
        while anzahl_versteckt < 4:
            i+=1
            if i == 7000:
                i = 0
                self.ping_remote(0, 0, 7, self.num, self.gameid)   # Sag dem Gegner, dass er nichts machen soll. Timeout verhindern
                connection.Pump()
                self.Pump()
            event1 = pygame.event.get()
            if len(event1) > 0:
                for event in event1:
                    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        if language == "de":
                            print("Spieler hat beendet")
                        else:
                            print("Player has finished")
                        return False

                    if event.type == pygame.KEYDOWN and event.type != QUIT:
                        self.chatinput(event.unicode[:1])

                    if event.type == QUIT:
                        return False
                    elif event.type == MOUSEBUTTONDOWN:
                        x = pygame.mouse.get_pos()[0]
                        y = pygame.mouse.get_pos()[1]
                        xpos, ypos = chatfensterposition(x,y)
                        xpos = int(xpos)
                        ypos = int(ypos)
                        mouse_presses = pygame.mouse.get_pressed()
                        if xpos < 9 and ypos < 7:
                            if mouse_presses[2] or mouse_presses[0]:
                                if self.galaxis[ypos][xpos]==6:
                                    raumschiff_zeichnen(xpos,ypos,WEISS)
                                    self.galaxis[ypos][xpos] = 5
                                    anzahl_versteckt+=1
                                elif self.galaxis[ypos][xpos]==5:
                                    self.galaxis[ypos][xpos] = 6
                                    anzahl_versteckt-=1
                                    self.raumschiff_loeschen()
                                    self.chatausgabe("")
                                    self.inputbox_zeichnen("", False)
                                    userinfo(info)
                                    userinfotext(self.old_string, self.old_string2)

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
        userinfotext(verfugbar, besetzt)
        self.spielerbereit = True

        return True

    def GegnerWaehlen(self):
        self.gegner_verbunden = True
        self.Send({"action": "spieler_bereit", "num": self.num, "gameid": self.gameid, "userid": self.userid, "bereit": self.spielerbereit})
        if language == "de":
            text = "Wähle einen Gegner:"
        else:
            text = "Choose an opponent:"
        text = font2.render(text, True, (255, 0, 0))
        pygame.draw.rect(fenster, SCHWARZ, [kor(17.5), kor(29.25),kor(30),kor(1.2)], 0)
        fenster.blit(text, ([kor(17.6), kor(29.5)]))
        pygame.draw.rect(fenster, SCHWARZ, [kor(25.4), kor(29.25),kor(30),kor(1.4)], 0)
        pygame.draw.rect(fenster, BLAU, [kor(25.5), kor(29.25),kor(10.3),kor(1.2)], 1)
        self.inputbox_zeichnen("", True)
#        pygame.event.set_grab(True)         # Maus in Fenster einsperren
        while True:
            text = ""
            pg.key.set_repeat()
            while len(text) < 3:
                run = True
                text_surf = font.render("_", True, (255, 0, 0))
                fenster.blit(text_surf, ([kor(25.6), kor(29.376)]))
                while run:
                    clock.tick(60)
                    event1 = pygame.event.get()
                    if len(event1) > 0:
                        for event in event1:
                            if event.type == pygame.QUIT:
                                run = False
                                text = ""
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    return False, False
                                if event.key == pygame.K_RETURN:
                                    run = False
                                elif event.key == pygame.K_BACKSPACE:
                                    text =  text[:-1]
                                else:
                                    text += event.unicode[:1]
                                text_surf = font.render(text+"_", True, (255, 0, 0))
                                pygame.draw.rect(fenster, SCHWARZ, [kor(25.6), kor(29.35),kor(10.1),kor(1)], 0)
                                fenster.blit(text_surf, ([kor(25.6), kor(29.376)]))
                            x = pygame.mouse.get_pos()[0]
                            y = pygame.mouse.get_pos()[1]
                            mouse_presses = pygame.mouse.get_pressed()
                            xpos, ypos = chatfensterposition(x,y)
                            xpos = int(xpos)
                            ypos = int(ypos)
                            if xpos > 8:
                                if mouse_presses[2] or mouse_presses[0]:
                                    self.chatinput("")
                                    self.inputbox_zeichnen("", True)
                    connection.Pump()
                    self.Pump()
                    pygame.display.flip()
                    if self.running:
                        return False, True
            pygame.draw.rect(fenster, SCHWARZ, [kor(17.5), kor(29.25),kor(30),kor(1.2)], 0)
            pygame.draw.rect(fenster, SCHWARZ, [kor(25.4), kor(29.25),kor(30),kor(1.4)], 0)
            return "gegner=" + text, True


##### Grundsätzliche Aufrufe

galax=GalaxisGame(nickname, bg_image) # __init__ wird hier aufgerufen

while True:

    if restarted:
        bg_image = galax.Neustart()

    # Spielfeld erzeugen über Berechnung

    fenster = pygame.display.set_mode((56 * MULTIPLIKATOR, 33 * MULTIPLIKATOR))

    # Titel für Fensterkopf
    if language == "de":
        fenstertitel = "GALAXIS electronic   (ESC zum verlassen)"
    else:
        fenstertitel = "GALAXIS electronic   (ESC to exit)"
    pygame.display.set_caption(fenstertitel)
    spielfeld_zeichnen(bg_image)

    connection.Pump()
    galax.Pump()

    mein_name = str(galax.mein_name_retour())       # Nickname an Server senden und Server Antwort holen


    # Raumschiffe verstecken

    if language == "de":
        print("Wenn Du fertig versteckt hast, wähle einen Gegner aus.")
        print("ESC im Spielfenster zum verlassen.")
        info = mein_name + ", verstecke Deine 4 Raumschiffe"
    else:
        print("When you have finished hiding, choose an opponent.")
        print("ESC in game window to exit.")
        info = mein_name + ", hide your 4 spaceships"
    userinfo(info)

    if galax.Verstecken(info) is False:
        pygame.quit()
        sys.exit()

    erfolg = False                                                          # Info:
    gegner_verbunden = True                                                 # - False   False = Abgebrochen
    while gegner_verbunden:                                                 # - False   True  = Von anderem Spieler aufgerufen
        while erfolg is False:                                              # - !=False True  = selber Gegner ausgewählt
            gegner, erfolg = galax.GegnerWaehlen()
            if erfolg is False:                                             # False   False = Gegnerwahl abgebrochen:
                if language == "de":
                    print("Spiel abgebrochen")
                else:
                    print("Game aborted")
                gegner_verbunden = False
                break
            if gegner is False and erfolg:                          # False   True  = Von anderem Spieler aufgerufen
                break
            if gegner is not False and erfolg:                          # !=False True  = selber Gegner ausgewählt
                connection.Send({"action": "message", "message": gegner, "gameid": -1, "user": mein_name})
            erfolg = galax.Warten()

        if gegner_verbunden:
            spiel_fertig = galax.Galaxis()                                  #### Spiel starten
            if spiel_fertig is False:                                       # Wenn Spiel abgebrochen:
                if language == "de":
                    print("Spiel abgebrochen")
                else:
                    print("Game aborted")
                break
            if spiel_fertig is True:                                        # Wenn Spiel fertig:
                if language == "de":
                    print("Spiel fertig")
                else:
                    print("Game finished")
                break

    #### Spiel neu starten?
    ja_nein_zeichnen(0)

    # Fenster aktualisieren und Online-User Anzeige löschen
    if language == "de":
        userinfotext(["Momentan keine Information verfügbar"], ["Momentan keine Information verfügbar"])
    else:
        userinfotext(["No information available at the moment"], ["No information available at the moment"])

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
        restarted = True
    else:
        break

connection.Send({"action": "UserSchliessen"})
time.sleep(1)
connection.Close()
pygame.quit()
sys.exit()


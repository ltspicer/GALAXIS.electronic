#!/usr/bin/python3

###############################
#  GALAXIS electronic V7.1    #
#   von Daniel Luginbuehl     #
#         (C) 2024            #
# webmaster@ltspiceusers.ch   #
#       Python updater        #
###############################

from ftplib import FTP, error_perm
import os
import sys
import time
import shutil

my_os=sys.platform
print()
print("Your OS is", my_os)
print()

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
                print(f"Skipping download of {item} because Windows == {win}")
                continue
            # Überspringe den Download von 'galaxis', wenn 'unix' False ist
            if item == "galaxis" and not unix:
                print(f"Skipping download of {item} because Unix == {unix}")
                continue
            # Überspringe den Download von 'galaxis.py', wenn 'pyt' False ist
            if item == "galaxis.py" and not pyt:
                print(f"Skipping download of {item} because Python == {pyt}")
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

# Exists Binary and Python file?

unix, win, pyt = False, False, False
unix1, win1, pyt1 = False, False, False
if os.path.isfile("galaxis"):
    unix1 = True
if os.path.isfile("galaxis.exe"):
    win1 = True
if os.path.isfile("galaxis.py"):
    pyt1 = True

if pyt1 and (win1 or unix1):
    print("Nebst der Python Variante ist auch installiert:")
    print("In addition to the Python variant is also installed:")
    print()
    if win1: print("Windows exe")
    if unix1: print("Linux Binary")
    print()
    print("Welche soll ich behalten?")
    print("Which ones should I keep?")
    print("A = Alle, L = nur Linux Binary,  W = nur Windows exe,  P = nur Python Variante, Q = Abbruch")
    print("A = All,  L = Linux binary only, W = Windows exe only, P = Python variant only, Q = Quit")
    print()
    
    while True:
        answer = input("Wähle/Select: ").strip()
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
            sys.exit()
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
move_all_files('new_release', '.')

# Build starter.sh for Linux binary
if unix:
    print("Build starter.sh")
if unix and not pyt:
    with open("starter.sh", "w") as f:
        f.write("#!/bin/sh\n\n")
        f.write("export LD_PRELOAD=/usr/lib64/libstdc++.so.6\n")
        f.write("export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6\n\n")
        f.write('HOME="$(getent passwd $USER | awk -F \':\' \'{print $6}\')"\n')
        f.write('cd ${HOME}/galaxis.electronic.linux ; ./galaxis # Hier ggf. Pfad innerhalb des home Verzeichnisses anpassen !!!\n')

if unix and pyt:
    with open("starter.sh", "w") as f:
        f.write("#!/bin/sh\n\n")
        f.write("export LD_PRELOAD=/usr/lib64/libstdc++.so.6\n")
        f.write("export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6\n\n")
        f.write('HOME="$(getent passwd $USER | awk -F \':\' \'{print $6}\')"\n')
        f.write('cd ${HOME}/galaxis.electronic.linux ; ./galaxis\n\n')
        f.write('#### starter for Python variant is different!!:\n\n')
        f.write('#HOME="$(getent passwd $USER | awk -F \':\' \'{print $6}\')"\n')
        f.write('#cd ${HOME}/galaxis.electronic ; ./galaxis.py # Hier ggf. Pfad innerhalb des home Verzeichnisses anpassen !!!\n')

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

# Remove temp directory
print("Remove temp directory")
shutil.rmtree("new_release", ignore_errors=True)

# Finish
print()
print("Info:")
print("If pip returns the error 'externally-managed-environment', see:")
print("https://www.makeuseof.com/fix-pip-error-externally-managed-environment-linux/")
print()
print("Press RETURN if this window doesn't close!")

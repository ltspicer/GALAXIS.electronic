#!/bin/sh

HOME="$(getent passwd $USER | awk -F ':' '{print $6}')"
cd ${HOME}/galaxis.electronic   # Hier ggf. Pfad innerhalb des home Verzeichnisses anpassen !!!
./galaxis.py

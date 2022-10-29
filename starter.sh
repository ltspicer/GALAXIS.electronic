#!/bin/sh

HOME="$(getent passwd $USER | awk -F ':' '{print $6}')"
cd ${HOME}/galaxis.electronic ; ./galaxis.py  # Hier ggf. Pfad innerhalb des home Verzeichnisses anpassen !!!

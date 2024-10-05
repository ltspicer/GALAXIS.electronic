#!/bin/sh

HOME="$(getent passwd $USER | awk -F ':' '{print $6}')"
cd ${HOME}/galaxis.electronic ; ./galaxis.py  # Hier ggf. Pfad innerhalb des home Verzeichnisses anpassen !!!

#### starter for Linux binary is different!!:

#export LD_PRELOAD=/usr/lib64/libstdc++.so.6
#export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
#
#HOME="$(getent passwd $USER | awk -F ':' '{print $6}')"
#cd ${HOME}/galaxis.electronic.linux ; ./galaxis   # Hier ggf. Pfad innerhalb des home Verzeichnisses anpassen !!!

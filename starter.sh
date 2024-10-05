#!/bin/sh

HOME="$(getent passwd $USER | awk -F ':' '{print $6}')"
cd ${HOME}/galaxis.electronic   # Hier ggf. Pfad innerhalb des home Verzeichnisses anpassen !!!
./galaxis.py

#### starter for Linux binary is different!!:

#export LD_PRELOAD=/usr/lib64/libstdc++.so.6
#export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
#
#./galaxis

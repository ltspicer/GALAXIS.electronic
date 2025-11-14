#!/bin/sh

HOME="$(cd -- "$(dirname -- "$0")" && pwd)"
cd ${HOME} ; ./galaxis.py

#### starter for Linux binary is different!!:

#export LD_PRELOAD=/usr/lib64/libstdc++.so.6
#export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
#
#HOME="$(cd -- "$(dirname -- "$0")" && pwd)"
#cd ${HOME} ; ./galaxis

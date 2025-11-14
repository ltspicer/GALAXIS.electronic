#!/bin/sh

if [ ! -f config.ini ]; then
    cat << 'EOF' > config.ini
[DEFAULT]
multiplikator = 25
language = de
nick = -
spielmodus = 2
hostaddr = galaxis.game-host.org
hostport = 10002
local_hiscore = 0

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

EOF
fi

export LD_PRELOAD=/usr/lib64/libstdc++.so.6
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6

HOME="$(getent passwd $USER | awk -F ':' '{print $6}')"
cd ${HOME}/galaxis.electronic.linux ; ./galaxis # Hier ggf. Pfad anpassen !!!

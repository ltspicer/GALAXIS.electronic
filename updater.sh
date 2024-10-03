#!/bin/bash

###############################
#  GALAXIS electronic V6.2    #
#   von Daniel Luginbuehl     #
#         (C) 2024            #
# webmaster@ltspiceusers.ch   #
#      unix updater.sh        #
###############################


# killall -9 "galaxis.py"

# URL to repo
url="https://github.com/ltspicer/GALAXIS.electronic/tarball/master"
#url_rls="https://github.com/ltspicer/GALAXIS.electronic/releases/download/V4.7/galaxis"


# Exists Binary and Python file?
if [ -f "galaxis" ] && [ -f "galaxis.py" ] ; then
    echo -e "Es ist die Linux Binary und Python Variante installiert. Welche soll ich behalten?"
    echo -e "\033[44mb\033[0m = beide, \033[44ml\033[0m = nur Linux Binary, \033[44mp\033[0m = nur Python Variante"
    echo
    echo "The Linux binary and the Python version are installed. Which one should I keep?"
    echo -e "\033[44mb\033[0m = both, \033[44ml\033[0m = Linux binary only, \033[44mp\033[0m = Python variant only"
    while true; do
        read  -t 15 -r -p "In 15 Sekunden wird fortgefahren / The process will continue in 15 seconds " answer
        if echo "$answer" | grep -iq "^b" ;then
	        break
        fi
        if echo "$answer" | grep -iq "^l" ;then
			rm galaxis.py
	        break
        fi
        if echo "$answer" | grep -iq "^p" ;then
			rm galaxis
	        break
        fi
        if echo "$answer" == "" ;then
	        break
        fi
    done
fi

# Exist compiled galaxis file? 
if [ -f "galaxis" ] && [ ! -f "galaxis.py" ] ; then
    # Wright the starter.sh for Linux binary start
    compiled=1
    echo "#!/bin/sh" > starter.sh
    echo "" >> starter.sh
    echo "export LD_PRELOAD=/usr/lib64/libstdc++.so.6" >> starter.sh
    echo "export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6" >> starter.sh
    echo "" >> starter.sh
    echo "HOME=\"\$(getent passwd \$USER | awk -F ':' '{print \$6}')\"" >> starter.sh
    echo 'cd ${HOME}/galaxis.electronic.linux ; ./galaxis # Hier ggf. Pfad innerhalb des home Verzeichnisses anpassen!' >> starter.sh
else
    compiled=0
fi

if [ -d "pygame" ] ; then
    pygame=1
else
    pygame=0
fi

# Use curl or wget, depending on which one we find
if hash curl 2>/dev/null
then
    curl_or_wget="curl -L $url -o main.tgz"
#    curl_wget_rls="curl -L $url_rls -o galaxis"
elif hash wget 2>/dev/null
then
    curl_or_wget="wget $url -O main.tgz"
#    curl_wget_rls="wget $url_rls -O galaxis"
fi

if [ -z "$curl_or_wget" ]; then
        echo "Neither curl nor wget found. Cannot use http method." >&2
        exit 1
fi

# Download repo and unpack
rm -rf new_release 2>/dev/null
mkdir new_release
cd new_release
$($curl_or_wget)
tar -xvf main.tgz

# Move directories
cd ltspicer-GALAXIS.electronic*
mv * ../
cd ..
rm ../updater.bat 2>/dev/null
rm -rf ../data 2>/dev/null
rm -rf ../PodSixNet 2>/dev/null
rm -rf ../asyncore 2>/dev/null
rm -rf ../asynchat 2>/dev/null
if [[ $pygame -eq 1 ]] ; then
    rm -rf ../pygame 2>/dev/null
    rm -rf ../pygame.libs 2>/dev/null
    rm -rf ../pygame-2.6.0.data 2>/dev/null
fi

# Move files

movables=(Anleitung.txt README.md galaxis.py)

for move in "${movables[@]}" ; do
    mv $move ../ 2>/dev/null
done
mv updater.sh ../updater_tmp.sh

# Move required files (binary or Python)
if [[ $compiled -ne 1 ]] ; then
    mv starter.sh ../
    if [[ $pygame -eq 1 ]] ; then
        unzip pygame/pygame.zip -d ../pygame    # unzip pygame.zip to pygame directory
    fi
else

# Move compiled file
    mv galaxis ../
fi

# Move data, PodSixNet, asyncore and asynchat to game root folder
mv data ../
if [[ $compiled -eq 0 ]] ; then
    mv PodSixNet ../
    mv asyncore ../
    mv asynchat ../
fi
if [[ $pygame -eq 1 ]] ; then
    #mv pygame ../
    mv pygame.libs ../
    mv pygame-2.6.0.data ../
fi

# Remove temp directories and make the game file executable
cd ..
rm -rf new_release
if [[ $compiled -eq 1 ]] ; then
    rm galaxis.py 2>/dev/null
    rm -rf pygame 2>/dev/null
    rm -rf pygame.libs 2>/dev/null
    rm -rf pygame-2.6.0.data 2>/dev/null
    chmod +x galaxis
else
    chmod +x galaxis.py
fi

# Make executable
chmod +x starter.sh
chmod +x updater_tmp.sh

# Finish
echo
echo "If pip returns the error 'externally-managed-environment', see:"
echo "https://www.makeuseof.com/fix-pip-error-externally-managed-environment-linux/"
echo
sleep 5
echo "Press RETURN if this window doesn't close!"
mv updater_tmp.sh updater.sh 2> /dev/null & exit 0


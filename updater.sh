#!/bin/bash

###############################
#  GALAXIS electronic V5.8    #
#  von Daniel Luginbuehl      #
#        (C) 2024             #
# webmaster@ltspiceusers.ch   #
#       unix updater.sh       #
###############################


# killall -9 "galaxis.py"

# URL to repo
url="https://github.com/ltspicer/GALAXIS.electronic/tarball/master"
#url_rls="https://github.com/ltspicer/GALAXIS.electronic/releases/download/V4.7/galaxis"

# Exist compiled galaxis file? 
if [ -f "galaxis" ] && [ ! -f "galaxis.py" ] ; then
    compiled=1
else
    compiled=0
fi
if [ -f "config.ini" ] ; then
    config=1
else
    config=0
fi
if [ -d "pygame" ] ; then
    pygame=1
else
    pygame=0
fi

# use curl or wget, depending on which one we find
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

# Download repo
rm -rf new_release
mkdir new_release
cd new_release
$($curl_or_wget)
#if [[ $compiled -eq 1 ]] ; then     # if compiled galaxis exists then download
#    $($curl_wget_rls)
#fi

tar -xvf main.tgz
cd ltspicer-GALAXIS.electronic*
mv * ../
cd ..
rm ../updater.bat
rm -rf ../data
rm -rf ../PodSixNet
rm -rf ../asyncore
rm -rf ../asynchat
rm -rf ../pygame.libs
rm -rf ../pygame-2.6.0.data
if [[ $pygame -eq 1 ]] ; then
    rm -rf ../pygame
fi

# Move files
if [[ $config -eq 1 ]] ; then
    movables=(Anleitung.txt README.md galaxis.py)
else
    movables=(Anleitung.txt README.md galaxis.py config.ini)
fi

for move in "${movables[@]}" ; do
    mv $move ../
done
mv updater.sh ../updater_tmp.sh

# Move required files (binary or Python)
if [[ $compiled -ne 1 ]] ; then
    mv starter.sh ../
    unzip pygame/pygame.zip -d ../pygame    # unzip pygame.zip to pygame directory
else
# Move compiled file
    mv galaxis ../
fi

# Move data, PodSixNet, asyncore and asynchat to game root folder
mv data ../
mv PodSixNet ../
mv asyncore ../
mv asynchat ../
#mv pygame ../
mv pygame.libs ../
mv pygame-2.6.0.data ../

cd ..
rm -rf new_release
if [[ $compiled -eq 1 ]] ; then
    rm -rf galaxis.py
    rm -rf PodSixNet
    rm -rf asyncore
    rm -rf asynchat
    rm -rf pygame
    rm -rf pygame.libs
    rm -rf pygame-2.6.0.data
    chmod +x galaxis
else
    chmod +x galaxis.py
fi

# Make executable
chmod +x starter.sh
chmod +x updater_tmp.sh

echo
echo "If pip returns the error 'externally-managed-environment', see:"
echo "https://www.makeuseof.com/fix-pip-error-externally-managed-environment-linux/"
echo
sleep 5
echo "Press RETURN if this window doesn't close!"
mv updater_tmp.sh updater.sh 2> /dev/null & exit 0


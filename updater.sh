#!/bin/bash


###############################
#  GALAXIS electronic V4.6    #
#  von Daniel Luginbuehl      #
#        (C) 2022             #
# webmaster@ltspiceusers.ch   #
#       unix updater.sh       #
###############################


killall -9 "galaxis.py"
# killall -9 "galaxis.exe"
url="https://github.com/ltspicer/GALAXIS.electronic/tarball/master"

# use curl or wget, depending on which one we find

if hash curl 2>/dev/null
then
    curl_or_wget="curl -L $url -o main.tgz"
elif hash wget 2>/dev/null
then
    curl_or_wget="wget $url -O main.tgz"
fi

if [ -z "$curl_or_wget" ]; then
        echo "Neither curl nor wget found. Cannot use http method." >&2
        exit 1
fi
rm -rf new_release
mkdir new_release
cd new_release
$($curl_or_wget)
tar -xvf main.tgz
cd ltspicer-GALAXIS.electronic*
mv * ../
cd ..
rm -rf ../data

movables=(config.ini Anleitung.txt README.md galaxis.py updater.bat starter.sh)

for move in "${movables[@]}" ; do
    mv $move ../
done
mv -v updater.sh ../updater_tmp.sh
mv data ../
cd ..
rm -rf new_release
chmod +x galaxis.py
# chmod +x galaxis.exe
chmod +x starter.sh
chmod +x updater_tmp.sh
chmod +x updater.bat
echo
echo "Press RETURN if this window doesn't close!"
mv updater_tmp.sh updater.sh 2> /dev/null & exit 0


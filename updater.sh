#!/bin/bash

###############################
#  GALAXIS electronic V4.8    #
#  von Daniel Luginbuehl      #
#        (C) 2022             #
# webmaster@ltspiceusers.ch   #
#       unix updater.sh       #
###############################


# killall -9 "galaxis.py"

# URL to repo
url="https://github.com/ltspicer/GALAXIS.electronic/tarball/master"
url_rls="https://github.com/ltspicer/GALAXIS.electronic/releases/download/V4.8/galaxis"

# Exist compiled galaxis file? 
if [ -f "galaxis" ] ; then
    compiled=1
else
    compiled=0
fi

# use curl or wget, depending on which one we find
if hash curl 2>/dev/null
then
    curl_or_wget="curl -L $url -o main.tgz"
    curl_wget_rls="curl -L $url_rls -o galaxis"
elif hash wget 2>/dev/null
then
    curl_or_wget="wget $url -O main.tgz"
    curl_wget_rls="wget $url_rls -O galaxis"
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
if [[ $compiled -eq 1 ]] ; then     # if compiled galaxis exists then download
    $($curl_wget_rls)
fi

tar -xvf main.tgz
cd ltspicer-GALAXIS.electronic*
mv * ../
cd ..
rm -rf ../data

# Move files
movables=(Anleitung.txt README.md galaxis.py)   #Insert config.ini if you want
for move in "${movables[@]}" ; do
    mv $move ../
done
mv updater.sh ../updater_tmp.sh

# Move required files (binary or Python)
if [[ $compiled -ne 1 ]] ; then
    mv starter.sh ../
    mv updater.bat ../
fi

# Move compiled file
if [[ $compiled -eq 1 ]] ; then
    mv galaxis ../
fi

# Move data directory
mv data ../

cd ..
rm -rf new_release
if [[ $compiled -eq 1 ]] ; then
    rm galaxis.py
    chmod +x galaxis
else
    chmod +x galaxis.py
fi

chmod +x starter.sh
chmod +x updater_tmp.sh
chmod +x updater.bat

echo
echo "Press RETURN if this window doesn't close!"
mv updater_tmp.sh updater.sh 2> /dev/null & exit 0


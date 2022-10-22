@echo off

echo:
echo ###############################
echo #  GALAXIS electronic V4.5    #
echo #  von Daniel Luginbuehl      #
echo #        (C) 2022             #
echo # webmaster@ltspiceusers.ch   #
echo #         updater.bat         #
echo #        Serveradresse        #
echo #    galaxis.game-host.org    #
echo ###############################
echo:

taskkill /F /IM galaxis.exe
set "DstFolder=%~dp0"
set "SrcFolder=%~dp0new_release\"
set "gitname=git-cmd.exe"
git --version
IF ERRORLEVEL 1 (
echo git is not installed. Please install first.
echo "Should I open the browser at the correct address (Y = Yes, Q = Quit)?"
For /f Delims^= %%G in ('choice /n /c:YQ')Do if /I "%%G"=="Y" goto:CONTINUE
goto END
:CONTINUE
start https://git-scm.com/download/win
echo "Is git installed (Y = Yes, Q = Quit)?"
For /f Delims^= %%G in ('choice /n /c:YQ')Do if /I "%%G"=="Y" goto:CONTINUE2
goto END
:CONTINUE2
echo "Reboot computer (Y = Yes, Q = Quit)?"
For /f Delims^= %%G in ('choice /n /c:YQ')Do if /I "%%G"=="Y" shutdown /r /t 0
goto END
)

rmdir /S /Q "new_release"
git clone https://github.com/ltspicer/GALAXIS.electronic.git new_release

echo **** Move data directory to the game root.
rmdir /S /Q "data"
move /Y %SrcFolder%data %DstFolder%data
IF %DstFolder:~-1%==\ SET DstFolder=%DstFolder:~0,-1%

echo **** Move all necessary files to the game root.
set "zu_kopierende_files[0]=config.ini"
set "zu_kopierende_files[1]=Anleitung.txt"
set "zu_kopierende_files[2]=README.md"
set "zu_kopierende_files[3]=galaxis.exe"
REM set "zu_kopierende_files[4]=updater.bat"

setlocal enabledelayedexpansion
for /l %%n in (0,1,3) do (
	echo !zu_kopierende_files[%%n]!
	move "!SrcFolder!!zu_kopierende_files[%%n]!" "!DstFolder!"
)

move %SrcFolder%updater.bat %DstFolder%\updater_tmp.bat

echo **** Remove temporary directory.
rmdir /S /Q "new_release"

start "galaxis" /separate galaxis.exe
echo **** galaxis restarted
echo:
echo **** Finished! You can now exit the updater by pressing RETURN. ****
move /Y updater_tmp.bat updater.bat

:END
exit /b 1
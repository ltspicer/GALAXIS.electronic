@echo off

echo:
echo ###############################
echo #  GALAXIS electronic V5.5    #
echo #  von Daniel Luginbuehl      #
echo #        (C) 2024             #
echo # webmaster@ltspiceusers.ch   #
echo #         updater.bat         #
echo #        Serveradresse        #
echo #    galaxis.game-host.org    #
echo ###############################
echo:

taskkill /F /IM galaxis.exe
taskkill /F /IM py.exe
taskkill /F /IM python.exe

for /f "tokens=4-7 delims=[.] " %%i in ('ver') do (
if %%i == Version set OSVersion=%%j.%%k
if %%i neq Version set OSVersion=%%i.%%j
)
set /a OSVersion=%OSVersion:.=%
if %OSVersion% gtr 99 (
	curl --version
	IF ERRORLEVEL 1 goto NOCURL
	rmdir /S /Q "new_release"
	mkdir new_release
	curl -L -o new_release\main.zip https://github.com/ltspicer/GALAXIS.electronic/archive/refs/heads/main.zip
	cd new_release
	tar -xf main.zip
	del main.zip
	cd..
	move /Y new_release\GALAXIS.electronic-main\data new_release\data
	move new_release\GALAXIS.electronic-main\*.* new_release
	rmdir /S /Q "new_release\GALAXIS.electronic-main"
	goto VERTEILEN
)

:NOCURL
git --version
IF ERRORLEVEL 1 (
	echo Unfortunately, CURL is not pre-installed before Windows 10, version 1803. That's why GIT needs to be installed.
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

:VERTEILEN
echo **** Move data and PodSixNet, asyncore and asynchat directory to the game root.
rmdir /S /Q "data"
rmdir /S /Q "PodSixNet"
move /Y new_release\data data
move /Y new_release\PodSixNet PodSixNet
move /Y new_release\asyncore asyncore
move /Y new_release\asynchat asynchat

echo **** Move all necessary files to the game root.
REM set "zu_kopierende_files[x]=config.ini"     REM less stay old version
set "zu_kopierende_files[0]=Anleitung.txt"
set "zu_kopierende_files[1]=README.md"
set "zu_kopierende_files[2]=galaxis.exe"
set "zu_kopierende_files[3]=galaxis.py"
set "zu_kopierende_files[4]=updater.sh"
REM set "zu_kopierende_files[5]=updater.bat"

setlocal enabledelayedexpansion
for /l %%n in (0,1,4) do (
	echo !zu_kopierende_files[%%n]!
	move "new_release\!zu_kopierende_files[%%n]!"
)

move new_release\updater.bat updater_tmp.bat

echo **** Remove temporary directory.
rmdir /S /Q "new_release"

echo:
echo **** Finished! You can now exit the updater by pressing RETURN. ****
move /Y updater_tmp.bat updater.bat & exit

:END
exit /b 1

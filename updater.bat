@echo off

echo:
echo ###############################
echo #  GALAXIS electronic V6.1    #
echo #   von Daniel Luginbuehl     #
echo #         (C) 2024            #
echo #  webmaster@ltspiceusers.ch  #
echo #        updater.bat          #
echo #       Serveradresse         #
echo #    galaxis.game-host.org    #
echo ###############################
echo:

taskkill /F /IM galaxis.exe 2>nul
taskkill /F /IM py.exe 2>nul
taskkill /F /IM python.exe 2>nul

if exist "pygame\" (
	set pygame=true
) else (
	set pygame=false
)

for /f "tokens=4-7 delims=[.] " %%i in ('ver') do (
if %%i == Version set OSVersion=%%j.%%k
if %%i neq Version set OSVersion=%%i.%%j
)
set /a OSVersion=%OSVersion:.=%
set "curl_git=keine"
rem goto NOCURL     rem  Auskommentieren, um git zu testen
if %OSVersion% gtr 99 (
    curl --version 2>nul
    IF ERRORLEVEL 1 goto NOCURL
	set "curl_git=curl"
    rmdir /S /Q "new_release" 2>nul
    mkdir new_release
    curl -L -o new_release\main.zip https://github.com/ltspicer/GALAXIS.electronic/archive/refs/heads/main.zip
	cd new_release
    tar -xf main.zip
    del main.zip 2>nul
    cd..
    move /Y new_release\GALAXIS.electronic-main\data new_release\data
    move /Y new_release\GALAXIS.electronic-main\PodSixNet new_release\PodSixNet
    move /Y new_release\GALAXIS.electronic-main\asyncore new_release\asyncore
    move /Y new_release\GALAXIS.electronic-main\asynchat new_release\asynchat
    if %pygame%==true (
        move /Y new_release\GALAXIS.electronic-main\pygame new_release\pygame
		move /Y new_release\GALAXIS.electronic-main\pygame-2.6.0.data new_release\pygame-2.6.0.data
		move /Y new_release\GALAXIS.electronic-main\pygame.libs new_release\pygame.libs
    )
    move new_release\GALAXIS.electronic-main\*.* new_release
    rmdir /S /Q "new_release\GALAXIS.electronic-main" 2>nul
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
) else (
	set "curl_git=git"
	rmdir /S /Q "new_release" 2>nul
	git clone https://github.com/ltspicer/GALAXIS.electronic.git new_release
)	

:VERTEILEN

setlocal enabledelayedexpansion

if exist "galaxis.exe" if exist "galaxis.py" (
    echo:
    echo Es ist die Windows.exe und Python Variante installiert. Welche soll ich behalten?
    echo b = beide, w = nur Windows exe, p = nur Python Variante
    echo.
    echo The Windows.exe and the Python version are installed. Which one should I keep?
    echo b = both, w = Windows.exe only, p = Python variant only
    echo.

    set "answer="

    :input_loop
    set /p answer="Waehle/Choose:"

    if /i "!answer!"=="b" (
        set compiled=2
        goto WEITERFAHREN
    ) else if /i "!answer!"=="w" (
        set compiled=1
        del galaxis.py 2>nul
        goto WEITERFAHREN
    ) else if /i "!answer!"=="p" (
        set compiled=0
        del galaxis.exe 2>nul
        goto WEITERFAHREN
    ) else if /i "!answer!"=="" (
        set compiled=2
        goto WEITERFAHREN
    )
    goto input_loop

) else if exist "galaxis.exe" (
    set compiled=1

) else (
    set compiled=0
)

:WEITERFAHREN

echo:
rmdir /S /Q "data" 2>nul
rmdir /S /Q "PodSixNet" 2>nul
rmdir /S /Q "asyncore" 2>nul
rmdir /S /Q "asynchat" 2>nul
rmdir /S /Q "pygame" 2>nul
rmdir /S /Q "pygame-2.6.0.data" 2>nul
rmdir /S /Q "pygame.libs" 2>nul
del "updater.sh" 2>nul
move /Y new_release\data data

if !compiled! neq 1 (
    echo **** Move data, PodSixNet, asyncore and asynchat directory to the game root.
    move /Y new_release\PodSixNet PodSixNet
    move /Y new_release\asyncore asyncore
    move /Y new_release\asynchat asynchat
	if !pygame!==true (
        echo **** Move necessary directories for pygame to the game root.
		move /Y new_release\pygame-2.6.0.data pygame-2.6.0.data
		move /Y new_release\pygame.libs pygame.libs
		if "!curl_git!"=="curl" (
            move /Y new_release\pygame pygame
			cd pygame
            tar -xf pygame.zip
			del "pygame.zip"
			cd..
		)
		if "!curl_git!"=="git" (
			tar --version 2>nul
			IF ERRORLEVEL 1 (
				echo **** No tar installed. Using git for downloading pygame.exe.
				git clone -b win_libs https://github.com/ltspicer/GALAXIS.electronic.git new_release\new_pygame
				move /Y new_release\new_pygame\pygame\pygame.exe .
				pygame.exe -y
				del pygame.exe
			) else (	
				move /Y new_release\pygame pygame
				cd pygame
				tar -xf pygame.zip
				del "pygame.zip"
				cd..
			)	
		)
	)	
)

echo **** Move all necessary files to the game root.

set "zu_kopierende_files[0]=Anleitung.txt"
set "zu_kopierende_files[1]=README.md"
if !compiled!==1 (
    set "zu_kopierende_files[2]=galaxis.exe"
	set "zu_kopierende_files[3]= "
)
if !compiled!==0 (
	set "zu_kopierende_files[2]= "
    set "zu_kopierende_files[3]=galaxis.py"
)
if !compiled!==2 (
    set "zu_kopierende_files[2]=galaxis.exe"
    set "zu_kopierende_files[3]=galaxis.py"
)

for /l %%n in (0,1,3) do (
	if "!zu_kopierende_files[%%n]!" neq " " (
		echo !zu_kopierende_files[%%n]!
		move "new_release\!zu_kopierende_files[%%n]!"
	)	
)

move new_release\updater.bat updater_tmp.bat

echo **** Remove temporary directory.
rmdir /S /Q "new_release"

echo:
echo **** Finished! You can now exit the updater by pressing RETURN. ****
move /Y updater_tmp.bat updater.bat & exit

:END
exit /b 1

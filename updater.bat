@echo off
set "DstFolder=%~dp0."
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

REM echo %SrcFolder% 
REM echo %DstFolder%

rmdir /S /Q "data"
move /Y %SrcFolder%data %DstFolder%\data

set zu_kopierende_files[0]=config.ini
set zu_kopierende_files[1]=Anleitung.txt
set zu_kopierende_files[2]=README.md
set zu_kopierende_files[3]=galaxis.exe
set zu_kopierende_files[4]=updater.bat
setlocal enabledelayedexpansion
for /l %%n in (0,1,4) do ( 
   move !SrcFolder!!zu_kopierende_files[%%n]! !DstFolder!
)

rmdir /S /Q "new_release"
		
:END
exit /b 1
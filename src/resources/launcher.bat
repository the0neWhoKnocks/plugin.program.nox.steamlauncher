@echo off

:: Process Chaining on Windows: Steam's `steam.exe` often acts as a bootstrapper
:: that spawns `steamwebhelper.exe` or another instance and exits immediately. A 
:: simple `subprocess.wait()` on `steam.exe` might return right away while Steam 
:: is still open.

:: Alternative: Instead of waiting on the PID, you can poll using `psutil` or 
:: loop while checking if the Steam window or main process name 
:: (`steam.exe` / `gameoverlayui.exe`) is active in the OS process list.

:: When Steam updates, the main steam.exe bootstrapper process often closes 
:: completely to let an updater binary swap out the files, and then launches a 
:: brand new steam.exe instance. If your Python script is strictly waiting on the 
:: original process ID (PID), it will think Steam has closed, launch Kodi 
:: prematurely, and leave you with both programs fighting for control.

set "TRAY_SCRIPT=%~1"
set "TRAY_ICON=%~2"
set "STEAM_PATH=%~3"
set "STEAM_BPM=%~4"
set "KODI_PATH=%~5"
set "KODI_PM=%~6"

:: TODO: Currently the tray icon stuff is buggy. Sometimes an icon is left behind and only goes away after a reboot.

:: :: Launch the system tray icon script in the background
:: if exist "%TRAY_SCRIPT%" (
::   start "" pythonw "%TRAY_SCRIPT%" "%TRAY_ICON%"
:: )

:: Launch Steam
start "" "%STEAM_PATH%" %STEAM_BPM%

:: Give Kodi time to close
timeout /t 2 /nobreak >nul

:: Monitor the Windows tasklist until Steam is closed
:LOOP
tasklist /FI "IMAGENAME eq steam.exe" 2>NUL | find /I /N "steam.exe">NUL
if "%ERRORLEVEL%"=="0" (
  timeout /t 2 /nobreak >nul
  goto LOOP
)

:: :: Steam has closed, kill the tray script
:: taskkill /F /FI "WINDOWTITLE eq Kodi Steam Launcher" >nul 2>&1
:: :: Kill pythonw if it's still running
:: taskkill /F /IM pythonw.exe >nul 2>&1

:: Start Kodi
start "" "%KODI_PATH%" "%KODI_PM%"
exit

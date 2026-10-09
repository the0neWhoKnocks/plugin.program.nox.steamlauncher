@echo off
:: 1. Launch Steam
start "" %1 %2

:: 2. Wait a few seconds for Kodi to finish shutting down completely
timeout /t 5 /nobreak >nul

:: 3. Loop and monitor the Windows tasklist until Steam is closed
:LOOP
tasklist /FI "IMAGENAME eq steam.exe" 2>NUL | find /I /N "steam.exe">NUL
if "%ERRORLEVEL%"=="0" (
  timeout /t 2 /nobreak >nul
  goto LOOP
)

:: 4. Steam has closed! Restart Kodi cleanly
start "" %3
exit

:: =============================================================================

@echo off
set "STEAM_PATH=%~1"
set "BPM_FLAG=%~2"
set "KODI_PATH=%~3"
set "TRAY_SCRIPT=%~4"
set "ICON_PATH=%~5"

:: 1. Launch the system tray icon script in the background using pythonw (no console window) [1]
if exist "%TRAY_SCRIPT%" (
  start "" pythonw "%TRAY_SCRIPT%" "%ICON_PATH%"
)

:: 2. Launch Steam [1]
start "" "%STEAM_PATH%" %BPM_FLAG%

:: 3. Give Kodi time to close completely [1]
timeout /t 5 /nobreak >nul

:: 4. Loop and monitor until Steam is closed [1]
:LOOP
tasklist /FI "IMAGENAME eq steam.exe" 2>NUL | find /I /N "steam.exe">NUL
if "%ERRORLEVEL%"=="0" (
  timeout /t 2 /nobreak >nul
  goto LOOP
)

:: 5. Steam has closed! Forcefully kill the background tray script [1]
taskkill /F /FI "WINDOWTITLE eq Kodi Steam Launcher Active" >nul 2>&1
:: Also close pythonw if it's running our specific script
taskkill /F /IM pythonw.exe >nul 2>&1

:: 6. Restart Kodi [1]
start "" "%KODI_PATH%"
exit

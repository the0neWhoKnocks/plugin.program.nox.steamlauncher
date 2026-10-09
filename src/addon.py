import os
import subprocess
import sys

import xbmc
import xbmcaddon
import xbmcvfs

# Process Chaining on Windows: Steam's `steam.exe` often acts as a bootstrapper
# that spawns `steamwebhelper.exe` or another instance and exits immediately. A 
# simple `subprocess.wait()` on `steam.exe` might return right away while Steam 
# is still open.
#
# Alternative: Instead of waiting on the PID, you can poll using `psutil` or 
# loop while checking if the Steam window or main process name 
# (`steam.exe` / `gameoverlayui.exe`) is active in the OS process list.

# When Steam updates, the main steam.exe bootstrapper process often closes 
# completely to let an updater binary swap out the files, and then launches a 
# brand new steam.exe instance. If your Python script is strictly waiting on the 
# original process ID (PID), it will think Steam has closed, launch Kodi 
# prematurely, and leave you with both programs fighting for control.

ADDON = xbmcaddon.Addon()

def launch_and_exit_kodi():
  steam_path = ADDON.getSetting("steam_path")
  if not steam_path:
    steam_path = r"C:\Program Files (x86)\Steam\steam.exe"
      
  use_bpm = "-bigpicture" if ADDON.getSetting("use_bpm") == "true" else ""
  kodi_path = sys.executable 

  # Gather paths for the batch file, tray script, and icon [1]
  addon_path = xbmcvfs.translatePath(ADDON.getAddonInfo('path'))
  batch_script = os.path.join(addon_path, "resources/launcher.bat")
  tray_script = os.path.join(addon_path, "resources/tray.py")
  icon_file = os.path.join(addon_path, "resources/media/tray.ico")

  try:
    xbmc.log("Steam Launcher: Passing control to external batch script with tray support...", level=xbmc.LOGINFO)
    
    if sys.platform == "win32":
      subprocess.Popen(
        [batch_script, steam_path, use_bpm, kodi_path, tray_script, icon_file], 
        shell=True, 
        creationflags=subprocess.CREATE_NEW_CONSOLE
      )
    
    xbmc.executebuiltin('Quit()')

  except Exception as err:  # noqa: BLE001
    xbmc.log(f"Steam Launcher Error: {err!s}", level=xbmc.LOGERROR)

if __name__ == '__main__':
  launch_and_exit_kodi()


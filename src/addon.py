import os
import subprocess
import sys

import xbmc
import xbmcaddon
import xbmcvfs

ADDON = xbmcaddon.Addon()

def launch_and_exit_kodi():
  steam_path = ADDON.getSetting("steam_path__win")
  steam_bpm = "-gamepadui" if ADDON.getSetting("steam_bpm") == "true" else ""
  kodi_path = ADDON.getSetting("kodi_path__win")
  kodi_pm = "-p" if ADDON.getSetting("kodi_portable_mode") == "true" else ""

  addon_path = xbmcvfs.translatePath(ADDON.getAddonInfo('path'))
  batch_script = os.path.join(addon_path, "resources/launcher.bat")
  tray_script = os.path.join(addon_path, "resources/tray.py")
  tray_icon = os.path.join(addon_path, "resources/media/tray.ico")

  try:
    xbmc.log("Steam Launcher: Passing control to external batch script with tray support...", level=xbmc.LOGINFO)
    
    if sys.platform == "win32":
      subprocess.Popen(
        [
          batch_script,
          tray_script,
          tray_icon,
          steam_path,
          steam_bpm,
          kodi_path,
          kodi_pm,
        ], 
        shell=True, 
        creationflags=subprocess.CREATE_NEW_CONSOLE
      )
    
    xbmc.executebuiltin('Quit()')

  except Exception as err:  # noqa: BLE001
    xbmc.log(f"Steam Launcher Error: {err!s}", level=xbmc.LOGERROR)

if __name__ == '__main__':
  launch_and_exit_kodi()

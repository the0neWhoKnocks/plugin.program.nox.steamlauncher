import ctypes
import os
import sys
import time
from ctypes import wintypes

# Win32 Constants for System Tray
NIM_ADD = 0x00000000
NIM_MODIFY = 0x00000001
NIM_DELETE = 0x00000002
NIF_ICON = 0x00000002
NIF_TIP = 0x00000004
IMAGE_ICON = 1
LR_LOADFROMFILE = 0x00000010

class NOTIFYICONDATA(ctypes.Structure):
  _fields_ = [
    ("cbSize", wintypes.DWORD),
    ("hWnd", wintypes.HWND),
    ("uID", wintypes.UINT),
    ("uFlags", wintypes.UINT),
    ("uCallbackMessage", wintypes.UINT),
    ("hIcon", wintypes.HANDLE),
    ("szTip", ctypes.c_char * 128),
    ("dwState", wintypes.DWORD),
    ("dwStateMask", wintypes.DWORD),
    ("szInfo", ctypes.c_char * 256),
    ("uTimeoutOrVersion", wintypes.UINT),
    ("szInfoTitle", ctypes.c_char * 64),
    ("dwInfoFlags", wintypes.DWORD),
  ]

def create_tray_icon(icon_path):
  shell32 = ctypes.windll.shell32
  user32 = ctypes.windll.user32

  # Load the .ico file
  hicon = user32.LoadImageW(None, icon_path, IMAGE_ICON, 0, 0, LR_LOADFROMFILE)
  
  nid = NOTIFYICONDATA()
  nid.cbSize = ctypes.sizeof(NOTIFYICONDATA)
  nid.hWnd = user32.GetDesktopWindow()
  nid.uID = 1
  nid.uFlags = NIF_ICON | NIF_TIP
  nid.hIcon = hicon
  nid.szTip = b"Kodi Steam Launcher"

  # Add to system tray
  shell32.Shell_NotifyIconA(NIM_ADD, ctypes.byref(nid))
  
  # try:
  #   # Keep process alive until main plugin terminates it
  #   while True:
  #     time.sleep(1)
  # finally:
  #   # Clean up icon when closed
  #   shell32.Shell_NotifyIconA(NIM_DELETE, ctypes.byref(nid))

if __name__ == "__main__":
  if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    create_tray_icon(sys.argv[1])

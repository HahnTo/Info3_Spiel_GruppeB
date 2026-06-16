# Global variables for the Menus
from pathlib import Path
import socket

TITLE = "Monster Jump"
FPS = 60

WIDTH = 1056
HEIGHT = 704

MENU_BGCOLOR = (216, 161, 123)

BASE_DIR = Path(__file__).resolve().parent
GRAPHICS_DIR = BASE_DIR / "graphics"
ASSETS_DIR = BASE_DIR / "assets"


def get_local_ip():
    """ Returns the local ip address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return f"IP nicht gefunden: {e}"
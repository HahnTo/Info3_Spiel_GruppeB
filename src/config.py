# Global variables for the Menus
from pathlib import Path
import socket

WIDTH = 1080
HEIGHT = 720

MENU_BGCOLOR = (216, 161, 123)


BASE_DIR = Path(__file__).resolve().parent
GRAPHICS_DIR = BASE_DIR / "graphics"
ASSETS_DIR = BASE_DIR / "assets"


def get_local_ip():
    """Gibt die lokale Netzwerk-IP zurück (nicht 127.0.0.1)."""
    try:
        # Verbindet sich nicht wirklich, nutzt nur das Routing um die richtige IP zu finden
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "IP nicht gefunden"
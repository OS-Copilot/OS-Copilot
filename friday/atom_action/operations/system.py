import sys

sys.dont_write_bytecode = True
from ..src import *
from ..query import screen

def sudo_install(package: str) -> None:
    return Pkexec_apt("install", package)

def pip_install(package: str) -> None:
    return pip("install", package)

def adjust_theme(theme: str) -> None:
    return gsettings("set", "org.gnome.desktop.interface", "gtk-theme", theme)

def adjust_brightness(brightness: int) -> None:
    assert brightness >= 0.5 and brightness <= 1
    brightness = str(brightness)
    return xrandr("--output", screen(), "--brightness", brightness)

# add by wzm
def terminal_show_file_content(path: str) -> None:
    return terminal('--geometry=130x44',"--", "bash", "-c", "cat {}; read line".format(path))

import os
import sys
from kivy.config import Config
from kivy.resources import resource_add_path
from kivy.utils import platform


def check_platform() -> None:
    if platform.lower() in ("linux", "macosx", "windows"):
        Config.set("graphics", "resizable", False)
        Config.set("graphics", "width", "1000")
        Config.set("graphics", "height", "800")
        Config.write()


if __name__ == "__main__":
    if hasattr(sys, "_MEIPASS"):
        resource_add_path(os.path.join(sys._MEIPASS))
    check_platform()

    from pong.game import PongApp
    PongApp().run()

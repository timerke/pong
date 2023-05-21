import importlib
import os
import sys
from kivy.config import Config
from kivy.resources import resource_add_path
from kivy.utils import platform


if "_PYIBoot_SPLASH" in os.environ and importlib.util.find_spec("pyi_splash"):
    import pyi_splash
    pyi_splash.close()


def check_platform() -> None:
    if platform.lower() in ("linux", "macosx", "win"):
        Config.set("graphics", "resizable", False)
        Config.set("graphics", "width", "1000")
        Config.set("graphics", "height", "800")
        Config.set("input", "mouse", "mouse,multitouch_on_demand")
        Config.set("postproc", "maxfps", "0")
        Config.write()


if __name__ == "__main__":
    if hasattr(sys, "_MEIPASS"):
        resource_add_path(os.path.join(sys._MEIPASS))
    check_platform()

    from pong.game import PongApp
    from pong.logger import set_logger
    set_logger()
    PongApp().run()

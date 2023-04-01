from kivy.utils import platform
from kivy.config import Config


def check_platform() -> None:
    if platform.system().lower() in ("linux", "macosx", "windows"):
        Config.set("graphics", "resizable", False)
        Config.set("graphics", "width", "1000")
        Config.set("graphics", "height", "800")
        Config.write()


if __name__ == "__main__":
    check_platform()

    from pong.game import PongApp
    PongApp().run()

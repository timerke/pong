import os
from kivy.app import App
from kivy.uix.widget import Widget
from pong.pong_game import PongGame
from pong.menu import GameType, Menu


class Game(Widget):
    """
    Class with main widget of application.
    """

    def __init__(self) -> None:
        super().__init__()
        self._menu: Menu = Menu()
        self._menu.bind(game_type=self.start_game)
        self._pong_game: PongGame = PongGame(self)

    def resize(self, root, _) -> None:
        for widget in (self._pong_game, self._menu):
            widget.pos = root.pos
            widget.size = root.size
            resize_func = getattr(widget, "resize", None)
            if resize_func:
                resize_func()

    def show_menu(self) -> None:
        self._menu.game_type = GameType.NOTHING
        try:
            self.add_widget(self._menu)
        except Exception:
            pass
        try:
            self.remove_widget(self._pong_game)
        except Exception:
            pass

    def start_game(self, menu: Menu, game_type: GameType) -> None:
        """
        :param menu: menu widget;
        :param game_type: type of game to start.
        """

        if game_type == GameType.NOTHING:
            return
        try:
            self.add_widget(self._pong_game)
        except Exception:
            pass
        try:
            self.remove_widget(self._menu)
        except Exception:
            pass
        self._pong_game.start_game(game_type)


class PongApp(App):
    """
    Class for application.
    """

    icon = os.path.join("media", "icon.png")

    def build(self) -> Game:
        """
        :return: main widget of application.
        """

        self.game = Game()
        return self.game

    def on_start(self) -> None:
        self.root.bind(size=self.game.resize)
        self.game.resize(self.root, None)
        self.game.show_menu()

import os
from kivy.app import App
from kivy.uix.widget import Widget
from pong.pong_game import PongGame
from pong.menu import Menu, GameType


class Game(Widget):

    def __init__(self) -> None:
        super().__init__()
        self._menu: Menu = Menu()
        self._menu.bind(game_type=self.start_game)
        self._pong_game: PongGame = PongGame()

    def resize(self, root, _) -> None:
        for widget in (self._pong_game, self._menu):
            widget.pos = root.pos
            widget.size = root.size
            resize_func = getattr(widget, "resize", None)
            if resize_func:
                resize_func()

    def show_menu(self) -> None:
        try:
            self.add_widget(self._menu)
        except Exception:
            pass
        try:
            self.remove_widget(self._pong_game)
        except Exception:
            pass

    def start_game(self, menu: Menu, game_type: GameType) -> None:
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

    def build(self) -> Game:
        self.icon = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "media", "pong.png")
        self.game = Game()
        return self.game

    def on_start(self) -> None:
        self.root.bind(size=self.game.resize)
        self.game.resize(self.root, None)
        self.game.show_menu()

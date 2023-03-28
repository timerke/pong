from enum import auto, Enum
from typing import Tuple
from kivy.app import App
from kivy.properties import Property
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout


class GameType(Enum):
    NOTHING = auto()
    AI = auto()
    SIMPLE_AI = auto()
    WITH_FRIEND = auto()


class Menu(FloatLayout):

    BACKGROUND_COLOR: Tuple[float, float, float, float] = (70 / 255, 130 / 255, 180 / 255, 1)
    FONT_SIZE: int = 35
    SIZE_HINT: Tuple[float] = (0.7, 0.2)
    game_type = Property(GameType.NOTHING)

    def __init__(self) -> None:
        super().__init__()
        self._button_play_with_friend: Button = Button(text="Играть с другом",
                                                       pos_hint={"center_x": 0.5, "center_y": 0.8})
        self._button_play_with_simple_ai: Button = Button(text="Играть с ИИ (простой уровень)",
                                                          pos_hint={"center_x": 0.5, "center_y": 0.6})
        self._button_play_with_ai: Button = Button(text="Играть с ИИ",
                                                   pos_hint={"center_x": 0.5, "center_y": 0.4})
        self._button_exit: Button = Button(text="Выход",
                                           pos_hint={"center_x": 0.5, "center_y": 0.2})
        for widget in (self._button_play_with_ai, self._button_play_with_friend, self._button_play_with_simple_ai,
                       self._button_exit):
            widget.font_size = Menu.FONT_SIZE
            widget.background_color = Menu.BACKGROUND_COLOR
            widget.size_hint = Menu.SIZE_HINT
            self.add_widget(widget)

        self._button_exit.bind(on_press=self.stop_app)
        self._button_play_with_ai.bind(on_press=self.start_ai_game)
        self._button_play_with_friend.bind(on_press=self.start_game_with_friend)
        self._button_play_with_simple_ai.bind(on_press=self.start_simple_ai_game)

    def start_ai_game(self, instance) -> None:
        self.game_type = GameType.AI

    def start_game_with_friend(self, instance) -> None:
        self.game_type = GameType.WITH_FRIEND

    def start_simple_ai_game(self, instance) -> None:
        self.game_type = GameType.SIMPLE_AI

    @staticmethod
    def stop_app(instance) -> None:
        App.get_running_app().stop()

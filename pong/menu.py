from enum import auto, Enum
from typing import List, Tuple
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import Property
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from version import VERSION


class GameType(Enum):
    AI = auto()
    NOTHING = auto()
    WITH_FRIEND = auto()


class Menu(FloatLayout):
    """
    Class for game menu.
    """

    BACKGROUND_COLOR: Tuple[float, float, float, float] = (208 / 255, 189 / 255, 244 / 255, 1)
    BUTTON_COLOR: Tuple[float, float, float, float] = (132 / 255, 88 / 255, 179 / 255, 1)
    BUTTON_COLOR_ON_HOVER: Tuple[float, float, float, float] = (160 / 255, 210 / 255, 235 / 255, 1)
    BUTTON_SIZE_HINT: Tuple[float, float] = (0.7, 0.16)
    game_type = Property(GameType.NOTHING)

    def __init__(self) -> None:
        super().__init__()
        self._button_play_with_friend: Button = Button(text="Play with friend",
                                                       pos_hint={"center_x": 0.5, "center_y": 0.81})
        self._button_play_with_friend.bind(on_press=self.start_game_with_friend)
        self._button_play_with_ai: Button = Button(text="Play with AI", pos_hint={"center_x": 0.5, "center_y": 0.6})
        self._button_play_with_ai.bind(on_press=self.start_ai_game)
        self._button_settings: Button = Button(text="Settings", pos_hint={"center_x": 0.5, "center_y": 0.39})
        self._button_settings.bind(on_press=self.change_settings)
        self._button_exit: Button = Button(text="Exit", pos_hint={"center_x": 0.5, "center_y": 0.18})
        self._button_exit.bind(on_press=self.stop_app)
        self._buttons: List[Button] = [self._button_play_with_friend, self._button_play_with_ai, self._button_settings,
                                       self._button_exit]
        for widget in self._buttons:
            widget.background_color = Menu.BUTTON_COLOR
            widget.size_hint = Menu.BUTTON_SIZE_HINT

        self._label_version: Label = Label(text=f"v{VERSION}", pos_hint={"center_x": 0.5, "center_y": 0.05})
        self._widgets: List = [*self._buttons, self._label_version]
        self.resize()
        Window.bind(mouse_pos=self._handle_mouse_hover)

    @staticmethod
    def _check_press(instance) -> bool:
        return instance.last_touch.device == "mouse" and instance.last_touch.button != "left"

    def _handle_mouse_hover(self, window, pos) -> None:
        """
        Method handles mouse movement over menu buttons.
        :param window: window;
        :param pos: mouse position.
        """

        for widget in self._buttons:
            if widget.collide_point(*pos):
                widget.background_color = Menu.BUTTON_COLOR_ON_HOVER
            else:
                widget.background_color = Menu.BUTTON_COLOR

    def _set_font_sizes(self, app_height: int) -> None:
        """
        :param app_height: height of application window.
        """

        for button in self._buttons:
            button.font_size = app_height * Menu.BUTTON_SIZE_HINT[1] * 0.6
        self._label_version.font_size = app_height * 0.05

    def change_settings(self, instance) -> None:
        if self._check_press(instance):
            return

    def on_size(self, *args) -> None:
        self._set_font_sizes(self.size[1])

    def resize(self) -> None:
        self.canvas.clear()
        with self.canvas:
            Color(*Menu.BACKGROUND_COLOR)
            Rectangle(pos=self.pos, size=self.size)
        for widget in self._widgets:
            try:
                self.remove_widget(widget)
            except Exception:
                pass
            self.add_widget(widget)

    def start_ai_game(self, instance) -> None:
        if self._check_press(instance):
            return
        self.game_type = GameType.AI

    def start_game_with_friend(self, instance) -> None:
        if self._check_press(instance):
            return
        self.game_type = GameType.WITH_FRIEND

    def stop_app(self, instance) -> None:
        if self._check_press(instance):
            return
        App.get_running_app().stop()

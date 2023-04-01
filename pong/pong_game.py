import math
import os
from random import randint
from typing import Tuple
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.vector import Vector
from pong.ball import Ball
from pong.headband import Headband
from pong.menu import GameType
from pong.player import AIPlayer, Player, Side, SimpleAIPlayer


class PongGame(Widget):

    BACKGROUND_COLOR: Tuple[float, float, float, float] = (53 / 255, 56 / 255, 57 / 255, 1)
    FONT_SIZE: int = 70
    ENEMY_COLOR: Tuple[float, float, float, float] = (160 / 255, 210 / 255, 235 / 255, 1)
    TIMEOUT: float = 1 / 60
    USER_COLOR: Tuple[float, float, float, float] = (229 / 255, 234 / 255, 245 / 255, 1)

    def __init__(self) -> None:
        super().__init__()
        self._ball: Ball = Ball()
        self._path_to_sound: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "media",
                                                "impact_on_ground.wav")
        self._sound: SoundLoader = SoundLoader.load(self._path_to_sound)
        self._schedule_event = None
        self._player_1: Player = None
        self._player_2: Player = None
        self._label_1: Label = Label()
        self._label_1.font_size = PongGame.FONT_SIZE
        self._label_2: Label = Label()
        self._label_2.font_size = PongGame.FONT_SIZE
        self._headband: Headband = Headband()
        self._headband.bind(start_round=self.start_round)

        with self.canvas:
            Color(*PongGame.BACKGROUND_COLOR)
            self._background: Rectangle = Rectangle(pos=self.pos, size=self.size)
            Color(1, 1, 1, 1)
            self._net: Rectangle = Rectangle(pos=[self.center_x - 5, 0], size=[10, self.height])

    def _init_ball(self) -> None:
        width, height = self.size
        self._ball.max_velocity = math.pow(width ** 2 + height ** 2, 0.5) * PongGame.TIMEOUT
        self._ball.init_velocity = self._ball.max_velocity / 5

    def _init_players(self, game_type: GameType) -> None:
        self._player_1 = Player(PongGame.USER_COLOR, Side.LEFT)
        self._player_1.bind(score=self.set_score)
        if game_type == GameType.AI:
            self._player_2 = AIPlayer(PongGame.ENEMY_COLOR, Side.RIGHT)
        elif game_type == GameType.SIMPLE_AI:
            self._player_2 = SimpleAIPlayer(PongGame.ENEMY_COLOR, Side.RIGHT)
        elif game_type == GameType.WITH_FRIEND:
            self._player_2 = Player(PongGame.ENEMY_COLOR, Side.RIGHT)
        self._player_2.bind(score=self.set_score)

    def on_touch_move(self, touch) -> None:
        for player in (self._player_1, self._player_2):
            player.change_position_by_touch(touch.x, touch.y)

    def set_score(self, player: Player, score: int) -> None:
        if player == self._player_1:
            self._label_1.text = str(score)
        elif player == self._player_2:
            self._label_2.text = str(score)

    def start_game(self, game_type: GameType) -> None:
        self._init_ball()
        self._init_players(game_type)
        self._player_1.score = 0
        self._player_2.score = 0

        self._init_round()

    def _init_round(self) -> None:
        if self._schedule_event:
            self._schedule_event.cancel()
        self._ball.center = self.center
        self._ball.velocity = Vector(self._ball.init_velocity, 0).rotate(randint(0, 360))

        self._player_1.x = self.x
        self._player_1.center_y = self.center_y
        self._player_2.x = self.width - self._player_2.width
        self._player_2.center_y = self.center_y

        self._background.pos = self.pos
        self._background.size = self.size
        self._net.pos = [self.center_x - 5, 0]
        self._net.size = [10, self.height]

        self._label_1.center_x = self.width / 4
        self._label_1.top = self.top - 50
        self._label_2.center_x = 3 * self.width / 4
        self._label_2.top = self.top - 50

        self._headband.center_x = self.center_x
        self._headband.center_y = self.center_y

        for widget in (self._ball, self._player_1, self._player_2, self._label_1, self._label_2, self._headband):
            if widget.parent is None:
                self.add_widget(widget)

        self._headband.start_countdown()

    def start_round(self, headband, start_round) -> None:
        if start_round:
            self._schedule_event = Clock.schedule_interval(self.update, PongGame.TIMEOUT)
            self.remove_widget(self._headband)

    def update(self, dt) -> None:
        for player in (self._player_1, self._player_2):
            player.change_position(self._ball)

        self._ball.move()
        self._player_1.hit_ball(self._ball)
        self._player_2.hit_ball(self._ball)

        if self._ball.y < 0 or self._ball.top > self.height:
            # Ball rebound from the horizontal borders of the field
            self._sound.play()
            self._ball.velocity_y *= -1

        new_round = False
        if self._ball.x < self.x:
            # The first player lost, add 1 point to the second player
            self._player_2.score += 1
            new_round = True
        elif self._ball.x > self.width:
            # The second player lost, add 1 point to the first player
            self._player_1.score += 1
            new_round = True
        if new_round:
            self._init_round()

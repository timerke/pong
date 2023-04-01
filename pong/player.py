import os
from enum import auto, Enum
from typing import Tuple
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from pong.ball import Ball


class Side(Enum):
    LEFT = auto()
    RIGHT = auto()


class Player(Widget):

    HIT_COLOR: Tuple[float, float, float, float] = (247 / 255, 89 / 255, 144 / 255, 1)
    INCREMENT_COEFFICIENT: float = 1.01
    score: NumericProperty = NumericProperty(-1)

    def __init__(self, rgb_color: Tuple[float, float, float, float], side: Side) -> None:
        super().__init__()
        self._color: Tuple[float, float, float, float] = rgb_color
        self._hit_was: int = 0
        self._path_to_sound: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "media",
                                                "hard_ball_hit.wav")
        self._sound: SoundLoader = SoundLoader.load(self._path_to_sound)
        self._side: Side = side
        self.size = [25, 200]
        self.bind(pos=self.move_racket)
        self._draw()

    def _change_position(self, new_y: float) -> None:
        if self.height / 2 < new_y < self.parent.height - self.height / 2:
            self.center_y = new_y
        elif new_y <= self.height / 2:
            self.center_y = self.height / 2
        elif new_y >= self.parent.height - self.height / 2:
            self.center_y = self.parent.height - self.height / 2

    def _draw(self, color: Tuple[float, float, float, float] = None) -> None:
        if color is None:
            color = self._color
        self.canvas.clear()
        with self.canvas:
            Color(*color)
            self._rect: Rectangle = Rectangle(pos=self.pos, size=self.size)

    def change_position(self, ball: Ball) -> None:
        pass

    def change_position_by_touch(self, touch_x: float, touch_y: float) -> None:
        if (self._side == Side.LEFT and touch_x < self.parent.width / 3) or \
                (self._side == Side.RIGHT and touch_x > 2 * self.parent.width / 3):
            self._change_position(touch_y)

    def hit_ball(self, ball: Ball) -> None:
        """
        Method to hit the ball with a racket.
        :param ball: ball.
        """

        if self._hit_was >= 1:
            self._hit_was += 1
        if self._hit_was > 5:
            self._draw()
            self._hit_was = 0
        if self.collide_widget(ball):
            if self._sound:
                self._sound.play()
            new_velocity = self.INCREMENT_COEFFICIENT * ball.velocity_module
            coefficient = self.INCREMENT_COEFFICIENT if ball.check_velocity_increasing(new_velocity) else 1
            velocity_x, velocity_y = ball.velocity
            ball.velocity = coefficient * Vector(-1 * velocity_x, velocity_y)
            if self._side == Side.LEFT:
                ball.center_x = self.right + ball.width / 2
            elif self._side == Side.RIGHT:
                ball.center_x = self.x - ball.width / 2
            self._draw(Player.HIT_COLOR)
            self._hit_was = 1

    def move_racket(self, obj, pos) -> None:
        self._rect.pos = pos


class SimpleAIPlayer(Player):

    VELOCITY: float = 4

    def __init__(self, rgb_color: Tuple[float, float, float, float], side: Side) -> None:
        super().__init__(rgb_color, side)
        self._player_velocity: float = SimpleAIPlayer.VELOCITY

    def change_position(self, ball: Ball) -> None:
        new_y = self.center_y + self._player_velocity
        if new_y <= self.height / 2 or new_y >= self.parent.height - self.height / 2:
            self._player_velocity *= -1
        self._change_position(new_y)

    def change_position_by_touch(self, touch_x: float, touch_y: float) -> None:
        pass


class AIPlayer(Player):

    VELOCITY: float = 4

    def __init__(self, rgb_color: Tuple[float, float, float, float], side: Side) -> None:
        super().__init__(rgb_color, side)
        self._player_velocity: float = SimpleAIPlayer.VELOCITY

    def change_position(self, ball: Ball) -> None:
        time = 0
        if ball.velocity_x < 0:
            time += 2 * (ball.center_x - self.width) / abs(ball.velocity_x)
        time += (self.parent.width - ball.center_x - self.width) / abs(ball.velocity_x)
        y_target = abs(ball.velocity_y * time)
        if ball.velocity_y < 0:
            y_target += self.parent.height - ball.center_y
        else:
            y_target += ball.center_y
        y_shift = int(abs(y_target)) % self.parent.height
        n_collisions = int(abs(y_target)) // self.parent.height
        if (n_collisions % 2 and ball.velocity_y > 0) or (n_collisions % 2 == 0 and ball.velocity_y < 0):
            y_required = self.parent.height - y_shift
        else:
            y_required = y_shift
        if y_required > self.center_y + self.height / 2:
            y_new = self.center_y + self._player_velocity
            self._change_position(y_new)
        elif y_required < self.center_y - self.height / 2:
            y_new = self.center_y - self._player_velocity
            self._change_position(y_new)

    def change_position_by_touch(self, touch_x: float, touch_y: float) -> None:
        pass

import logging
import random
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
    INCREMENT_COEFFICIENT: float = 1.08
    KEYBOARD_SHIFT: int = 30
    score: NumericProperty = NumericProperty(-1)

    def __init__(self, rgb_color: Tuple[float, float, float, float], side: Side) -> None:
        """
        :param rgb_color: color for player;
        :param side: side for player.
        """

        super().__init__()
        self._color: Tuple[float, float, float, float] = rgb_color
        self._hit_was: int = 0
        self._path_to_sound: str = os.path.join("media", "hard_ball_hit.wav")
        self._sound: SoundLoader = SoundLoader.load(self._path_to_sound)
        self._side: Side = side
        self.size = [25, 200]
        self.bind(pos=self.move_racket)
        self._draw()

    def _change_position(self, new_y: float) -> None:
        """
        :param new_y: new vertical position for player.
        """

        if self.height / 2 < new_y < self.parent.height - self.height / 2:
            self.center_y = new_y
        elif new_y <= self.height / 2:
            self.center_y = self.height / 2
        elif new_y >= self.parent.height - self.height / 2:
            self.center_y = self.parent.height - self.height / 2

    def _draw(self, color: Tuple[float, float, float, float] = None) -> None:
        """
        :param color: new color for player.
        """

        if color is None:
            color = self._color
        self.canvas.clear()
        with self.canvas:
            Color(*color)
            self._rect: Rectangle = Rectangle(pos=self.pos, size=self.size)

    def change_position(self, dt: float, ball: Ball) -> None:
        """
        Method changes position of player widget according to ball characteristics.
        :param dt:
        :param ball: ball.
        """

        pass

    def change_position_by_touch(self, touch_x: float, touch_y: float) -> None:
        """
        Method changes position of player widget by coordinated of touch.
        :param touch_x: horizontal coordinate;
        :param touch_y: vertical coordinate.
        """

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
            new_velocity = Player.INCREMENT_COEFFICIENT * ball.velocity_module
            coefficient = Player.INCREMENT_COEFFICIENT if ball.check_velocity_increasing(new_velocity) else 1
            velocity_x, velocity_y = ball.velocity
            ball.velocity = coefficient * Vector(-1 * velocity_x, velocity_y)
            if self._side == Side.LEFT:
                ball.center_x = self.right + ball.width / 2
            elif self._side == Side.RIGHT:
                ball.center_x = self.x - ball.width / 2
            self._draw(Player.HIT_COLOR)
            self._hit_was = 1

    def move_player_down(self) -> None:
        self._change_position(self.center_y - Player.KEYBOARD_SHIFT)

    def move_player_up(self) -> None:
        self._change_position(self.center_y + Player.KEYBOARD_SHIFT)

    def move_racket(self, obj, pos) -> None:
        """
        Method moves racket of player on window.
        :param obj:
        :param pos: position to place racket.
        """

        self._rect.pos = pos


class AIPlayer(Player):

    MAX_VELOCITY: float = 500
    MIN_VELOCITY: float = 1
    VELOCITY: float = 4

    def __init__(self, rgb_color: Tuple[float, float, float, float], side: Side) -> None:
        """
        :param rgb_color: color for player;
        :param side: side for player.
        """

        super().__init__(rgb_color, side)
        self._error: float = 0
        self._player_velocity: float = AIPlayer.VELOCITY

    def _calculate_ball_target_position(self, ball: Ball) -> Tuple[float, float]:
        """
        :param ball: ball.
        :return: vertical position of ball and time.
        """

        time = 0
        ball_center_x = (1 + self._error) * ball.center_x
        ball_center_y = (1 + self._error) * ball.center_y
        ball_velocity_x = (1 + self._error) * ball.velocity_x
        ball_velocity_y = (1 + self._error) * ball.velocity_y
        if ball.velocity_x < 0:
            time += 2 * (ball_center_x - self.width) / abs(ball_velocity_x)
        time += (self.parent.width - ball_center_x - self.width) / abs(ball_velocity_x)
        y_target = abs(ball_velocity_y * time)
        if ball_velocity_y < 0:
            y_target += self.parent.height - ball_center_y
        else:
            y_target += ball_center_y
        return y_target, time

    def change_player_error(self, opponent_score: int, max_score: int) -> None:
        """
        :param opponent_score: opponent's score;
        :param max_score: maximum score.
        """

        self._error = 0.1 if max_score != opponent_score + 1 else 0
        self._error *= 0.0 * random.random()
        logging.info("AI player has error = %.2f", self._error)

    def change_position(self, dt: float, ball: Ball) -> None:
        """
        Method changes position of player widget according to ball characteristics.
        :param dt:
        :param ball: ball.
        """

        y_target, time = self._calculate_ball_target_position(ball)
        y_shift = int(abs(y_target)) % self.parent.height
        n_collisions = int(abs(y_target)) // self.parent.height
        if (n_collisions % 2 and ball.velocity_y > 0) or (n_collisions % 2 == 0 and ball.velocity_y < 0):
            y_required = self.parent.height - y_shift
        else:
            y_required = y_shift

        if time != 0:
            required_velocity = abs(y_required - self.center_y) / time
            required_velocity = max(required_velocity, AIPlayer.MIN_VELOCITY)
            self._player_velocity = required_velocity

        if y_required > self.center_y + self.height / 2:
            y_new = self.center_y + self._player_velocity * dt
            self._change_position(y_new)
        elif y_required < self.center_y - self.height / 2:
            y_new = self.center_y - self._player_velocity * dt
            self._change_position(y_new)

    def change_position_by_touch(self, touch_x: float, touch_y: float) -> None:
        """
        Method changes position of player widget by coordinated of touch.
        :param touch_x: horizontal coordinate;
        :param touch_y: vertical coordinate.
        """

        pass

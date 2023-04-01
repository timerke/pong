import math
from kivy.graphics import Color, Ellipse
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector


class Ball(Widget):
    """
    Class for ball in game.
    """

    initial_velocity: float = None
    velocity_x = NumericProperty()
    velocity_y = NumericProperty()
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def __init__(self) -> None:
        super().__init__()
        self.size = [50, 50]
        with self.canvas:
            Color(1, 1, 1, 1)
            self._ellipse: Ellipse = Ellipse(size=self.size, pos=self.pos)
        self.bind(pos=self._move_ellipse)
        self.bind(velocity=self._change_color)

    def _change_color(self, obj, velocity) -> None:
        """
        Method changes color of ball depending on its velocity.
        :param obj: this object (instance of Ball class);
        :param velocity: new velocity of ball.
        """

        self.canvas.clear()
        with self.canvas:
            color = self.initial_velocity / self._get_velocity_module()
            Color(1 - color, 0, color, 1)
            self._ellipse = Ellipse(size=self.size, pos=self.pos)

    def _get_velocity_module(self) -> float:
        """
        :return: ball velocity module.
        """

        return math.pow((self.velocity_x**2 + self.velocity_y**2), 0.5)

    def _move_ellipse(self, obj, pos) -> None:
        self._ellipse.pos = pos

    def move(self) -> None:
        self.pos = Vector(*self.velocity) + self.pos

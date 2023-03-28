import math
from kivy.graphics import Color, Ellipse
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector


class Ball(Widget):

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
        self.bind(pos=self.move_ellipse)
        self.bind(velocity=self.change_color)

    def change_color(self, obj, velocity) -> None:
        self.canvas.clear()
        with self.canvas:
            color = self.initial_velocity / self.get_velocity_module()
            Color(1, color, color, 1)
            self._ellipse = Ellipse(size=self.size, pos=self.pos)

    def get_velocity_module(self) -> float:
        return math.pow((self.velocity_x**2 + self.velocity_y**2), 0.5)

    def move(self) -> None:
        self.pos = Vector(*self.velocity) + self.pos

    def move_ellipse(self, obj, pos) -> None:
        self._ellipse.pos = pos

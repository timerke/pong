from random import randint
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.vector import Vector
from pong.ball import Ball
from pong.player import AIPlayer, Player, Side, SimpleAIPlayer


class PongGame(Widget):

    def __init__(self) -> None:
        super().__init__()
        self._root = None
        self._ball: Ball = Ball()
        self._player_1: Player = Player([0, 1, 0, 1], Side.LEFT)
        self._player_1.bind(score=self.set_score)
        self._player_2: Player = AIPlayer([0, 0, 1, 1], Side.RIGHT)
        self._player_2.bind(score=self.set_score)
        self._label_1: Label = Label()
        self._label_1.font_size = 70
        self._label_2: Label = Label()
        self._label_2.font_size = 70
        with self.canvas:
            Color(1, 1, 1, 1)
            self._net: Rectangle = Rectangle(pos=[self.center_x - 5, 0], size=[10, self.height])

    def on_touch_move(self, touch) -> None:
        for player in (self._player_1, self._player_2):
            player.change_position_by_touch(touch.x, touch.y)

    def replace_widgets(self, root, _) -> None:
        self._label_1.center_x = root.width / 4
        self._label_1.top = root.top - 50
        self._label_2.center_x = 3 * root.width / 4
        self._label_2.top = root.top - 50

    def set_root(self, root) -> None:
        self._root = root

    def set_score(self, player: Player, score: int) -> None:
        if player == self._player_1:
            self._label_1.text = str(score)
        elif player == self._player_2:
            self._label_2.text = str(score)

    def start_game(self) -> None:
        self._player_1.score = 0
        self._player_2.score = 0
        self.start_round()

    def start_round(self, velocity: float = 4) -> None:
        """
        :param velocity: initial ball velocity.
        """

        self._ball.initial_velocity = velocity
        self._ball.center = self._root.center
        self._ball.velocity = Vector(velocity, 0).rotate(randint(0, 360))

        self._player_1.x = self._root.x
        self._player_1.center_y = self._root.center_y
        self._player_2.x = self._root.width - self._player_2.width
        self._player_2.center_y = self._root.center_y

        self._net.pos = [self._root.center_x - 5, 0]
        self._net.size = [10, self._root.height]

        self._label_1.center_x = self._root.width / 4
        self._label_1.top = self._root.top - 50
        self._label_2.center_x = 3 * self._root.width / 4
        self._label_2.top = self._root.top - 50

        if self._label_1.parent is None:
            self.add_widget(self._ball)
            self.add_widget(self._player_1)
            self.add_widget(self._player_2)
            self.add_widget(self._label_1)
            self.add_widget(self._label_2)

    def update(self, dt) -> None:
        for player in (self._player_1, self._player_2):
            player.change_position(self._ball)

        self._ball.move()
        self._player_1.hit_ball(self._ball)
        self._player_2.hit_ball(self._ball)

        if self._ball.y < 0 or self._ball.top > self.height:
            # Ball rebound from the horizontal borders of the field
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
            self.start_round()


class PongApp(App):

    def build(self) -> PongGame:
        self.game = PongGame()
        Clock.schedule_interval(self.game.update, 1 / 60)  # 60 FPS
        return self.game

    def on_start(self) -> None:
        self.game.set_root(self.root)
        self.root.bind(size=self.game.replace_widgets)
        self.game.start_game()

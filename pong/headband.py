import os
from random import random
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.properties import Property
from kivy.uix.label import Label


class Headband(Label):

    FONT_SIZE: int = 150
    START_NUMBER: int = 5
    return_to_menu: Property = Property(False)
    start_round: Property = Property(False)

    def __init__(self) -> None:
        super().__init__()
        self.font_size = Headband.FONT_SIZE
        self._number: int = None
        self._time: float = 0

    def _show_congratulations(self, dt) -> None:
        self._time += dt
        if self._time > 5:
            self.return_to_menu = True
        else:
            self.color = random(), random(), random(), 0.8

    def _show_countdown(self, dt) -> None:
        self._number -= 1
        if self._number == 0:
            self.text = "START"
        elif self._number > 0:
            self.text = str(self._number)
        elif self._number == -1:
            self._event.cancel()
            self.start_round = True

    def show_congratulations(self, winner: bool) -> None:
        self.return_to_menu = False
        self._time = 0
        self.color = 1, 0, 0, 0.8
        self.text = "You won!" if winner else "You lose!"
        self._event = Clock.schedule_interval(self._show_congratulations, 0.3)
        path_to_sound = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "media",
                                     "applause.wav" if winner else "sad_trombone.mp3")
        sound = SoundLoader.load(path_to_sound)
        sound.play()

    def start_countdown(self, start_number: int = None) -> None:
        self.start_round = False
        self.color = 1, 0, 0, 0.8
        self._number = start_number if start_number is not None else Headband.START_NUMBER
        self.text = str(self._number)
        self._event = Clock.schedule_interval(self._show_countdown, 1)

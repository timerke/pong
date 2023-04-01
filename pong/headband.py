from kivy.clock import Clock
from kivy.properties import Property
from kivy.uix.label import Label


class Headband(Label):

    FONT_SIZE: int = 150
    START_NUMBER: int = 5
    start_round: Property = Property(False)

    def __init__(self) -> None:
        super().__init__()
        self.color = 1, 0, 0, 0.8
        self.font_size = Headband.FONT_SIZE
        self._number: int = None

    def _show_countdown(self, dt) -> None:
        self._number -= 1
        if self._number == 0:
            self.text = "START"
        elif self._number > 0:
            self.text = str(self._number)
        elif self._number == -1:
            self._event.cancel()
            self.start_round = True

    def start_countdown(self, start_number: int = None) -> None:
        self.start_round = False
        self._number = start_number if start_number is not None else Headband.START_NUMBER
        self.text = str(self._number)
        self._event = Clock.schedule_interval(self._show_countdown, 1)

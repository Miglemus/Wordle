from abc import abstractmethod
from core.Game import Game


class Interface:
    def __init__(self):
        pass

    @abstractmethod
    def play(self) -> None:
        pass

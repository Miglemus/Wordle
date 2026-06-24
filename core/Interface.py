from abc import abstractmethod


class Interface:
    def __init__(self):
        pass

    @abstractmethod
    def play(self) -> None:
        pass

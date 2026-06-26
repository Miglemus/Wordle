from abc import ABC, abstractmethod


class GuessScorer(ABC):

    def __init__(self, guess: str, groups: list[int], possible_solutions: set):
        self._guess = guess
        self._groups = groups
        self._is_possible_solution = guess in possible_solutions

    @abstractmethod
    def __lt__(self, other):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    def __str__(self):
        return f"GuessScorer(guess={self._guess}, groups={self._groups}, is_possible_solution={self._is_possible_solution})"

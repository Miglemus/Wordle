import random
from core.Answer import Answer, Result
from core.utils import get_all_solutions, get_all_guesses, get_all_words


class Game:

    def __init__(self):
        self._solution = self.generate_random_solution()
        self._is_over = False

    def step(self, guess) -> Answer:
        answer = Answer.from_guess(guess, self._solution)
        if answer.is_correct():
            self._is_over = True
        return answer

    @property
    def is_over(self) -> bool:
        return self._is_over

    @staticmethod
    def generate_random_solution():
        return random.choice(list(get_all_solutions()))

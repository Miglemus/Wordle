import random
from core.Answer import Answer
from core.utils import get_all_solutions


class Game:

    def __init__(self):
        self._solution = self.generate_random_solution()
        self._is_over = False

    def step(self, guess) -> Answer:
        answer = Answer.from_guess(guess, self._solution)
        if answer.is_correct():
            self._is_over = True
        return answer

    def reset(self):
        self._solution = self.generate_random_solution()
        self._is_over = False

    def set_solution(self, solution):
        self._solution = solution
        self._is_over = False

    @property
    def is_over(self) -> bool:
        return self._is_over
    
    @staticmethod
    def generate_random_solution():
        return random.choice(list(get_all_solutions()))

import random
from core.Game import Game
from core.Solver import Solver
from core.utils import get_all_solutions


class Benchmark:
    def __init__(self, game: Game, solver: Solver):
        self._game = game
        self._solver = solver
        self._statistics = {}

    def run(self, num_solutions_tested: int = 200):
        self._game.reset()
        self._solver.reset()

        solutions_to_test = random.sample(list(get_all_solutions()), k=num_solutions_tested)
        for solution in solutions_to_test:
            self._game.set_solution(solution)
            answer = None
            num_guesses = 0
            while not self._game.is_over:
                guess = self._solver.guess(answer)
                answer = self._game.step(guess)
                num_guesses += 1

            self._statistics[solution] = num_guesses

    def print_statistics(self):
        total_guesses = sum(self._statistics.values())
        num_solutions = len(self._statistics)
        average_guesses = total_guesses / num_solutions
        print(f"Average number of guesses: {average_guesses:.2f}")
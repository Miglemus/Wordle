import random
from core.Game import Game
from core.Solver import Solver
from core.utils import get_all_solutions


class Benchmark:
    def __init__(self, game: Game, solver: Solver):
        self._game = game
        self._solver = solver
        self._statistics = {}

    def run(self, num_solutions_tested: int = 100000):
        solutions_to_test = random.sample(list(get_all_solutions()), k=max(1, min(num_solutions_tested, len(get_all_solutions()))))

        for solution in solutions_to_test:
            self._game.reset()
            self._solver.reset()
            self._game.set_solution(solution)

            answer = None
            num_guesses = 0
            while not self._game.is_over and num_guesses < 5:
                guess = self._solver.guess(answer)
                answer = self._game.step(guess)
                num_guesses += 1

            self._statistics[solution] = num_guesses
            print(f"Solution: {solution}, Guesses: {num_guesses}")
            
        self.print_statistics()

    def print_statistics(self):
        total_guesses = sum(self._statistics.values())
        num_solutions = len(self._statistics)
        average_guesses = total_guesses / num_solutions
        print(f"Average number of guesses: {average_guesses:.2f}")
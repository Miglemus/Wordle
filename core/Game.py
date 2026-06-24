import random


SOLUTION_FILE = "solutions.txt"
GUESSES_FILE = "wordle-guesses.txt"

class Game:

    def __init__(self):
        self._solution = self.generate_random_solution()

    def step(self, guess):
        return self.guess(guess, self._solution)

    @staticmethod
    def generate_random_solution():
        return random.choice(list(Game.get_all_solutions()))
    
    @staticmethod
    def get_all_solutions() -> set[str]:
        with open(SOLUTION_FILE, "r") as f:
            solutions = f.readlines()
        
        return {solution.strip().lower() for solution in solutions}

    @staticmethod
    def get_all_guesses() -> set[str]:
        with open(GUESSES_FILE, "r") as f:
            guesses = f.readlines()
        
        return {guess.strip().lower() for guess in guesses}

    @staticmethod
    def get_all_words() -> set[str]:
        return Game.get_all_solutions().union(Game.get_all_guesses())

    @staticmethod
    def guess(guess, solution):
        pass
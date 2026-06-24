import random


class Game:

    def __init__(self):
        self.solution = self.generate_random_solution()

    def step(self, guess):
        pass

    @staticmethod
    def generate_random_solution():
        return random.choice(Game.get_solution())
    
    @staticmethod
    def get_solution():
        with open("solutions.txt", "r") as f:
            solutions = f.readlines()
        
        return random.choice(solutions).strip().lower()

    @staticmethod
    def guess(guess, solution):
        pass
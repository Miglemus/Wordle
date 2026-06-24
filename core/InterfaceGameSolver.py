from core.Interface import Interface
from core.Game import Game
from core.Solver import Solver


class InterfaceGameSolver(Interface):
    
    def __init__(self, game: Game, solver: Solver):
        self._game = game
        self._solver = solver

    def play(self):
        guess = self._solver.guess(None)
        answer = self._game.step(guess)

        print(f"The solver guessed: '{guess}' with result:\n {answer}") 
        while not self._game.is_over:
            guess = self._solver.guess(answer)
            answer = self._game.step(guess)
            print(f"The solver guessed: '{guess}' with result:\n {answer}") 

        print(f"The solver has guessed the word correctly! Word: '{guess}'")

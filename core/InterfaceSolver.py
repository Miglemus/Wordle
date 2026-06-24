from core.Answer import Answer
from core.Interface import Interface
from core.Solver import Solver


class InterfaceSolver(Interface):

    def __init__(self, solver: Solver):
        self._solver = solver

    def play(self):
        guess = self._solver.guess(None)
        print(f"The solver guessed: '{guess}'")
        
        answer = input(f"Please provide the answer for '{guess}' (e.g., 'CPAAC'): ") 
        answer = Answer.from_string(answer, guess)

        while not answer.is_correct():
            guess = self._solver.guess(answer)
            print(f"The solver guessed: '{guess}'")
            answer = input(f"Please provide the answer for '{guess}' (e.g., 'CPAAC'): ") 
            answer = Answer.from_string(answer, guess)
        
        print(f"The solver has guessed the word correctly! Word: '{guess}'")

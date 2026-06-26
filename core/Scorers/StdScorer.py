from functools import total_ordering
from core.Scorers.GuessScorer import GuessScorer
import numpy as np


@total_ordering
class StdScorer(GuessScorer):

    def __init__(self, guess: str, groups: list[int], possible_solutions: set):
        super().__init__(guess, groups, possible_solutions)

    def __call__(self):
       return len(self._groups) / (1.0 + np.std(self._groups)) + (0.5 if self._is_possible_solution else 0)
    
    def __lt__(self, other: "StdScorer"):
        return self() < other()    

    def __eq__(self, other: "StdScorer"):
        return self() == other()
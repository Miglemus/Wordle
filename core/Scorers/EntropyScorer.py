from core.Scorers.GuessScorer import GuessScorer
from functools import total_ordering
import numpy as np


@total_ordering
class EntropyScorer(GuessScorer):

    def __init__(self, guess: str, group_sizes: list[int], possible_solutions: set):
        total_solutions = sum(group_sizes)
        self._entropy = 0.0
        
        for size in group_sizes:
            p = size / total_solutions
            self._entropy -= p * np.log2(p)
            
        self._is_possible_solution = guess in possible_solutions
        self._guess = guess

    def __call__(self):
        return self._entropy + (0.001 if self._is_possible_solution else 0)
    
    def __lt__(self, other: "EntropyScorer"):
        return self() < other()    

    def __eq__(self, other: "EntropyScorer"):
        return self() == other()
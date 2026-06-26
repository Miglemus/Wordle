from functools import total_ordering
from core.Scorers.GuessScorer import GuessScorer
import numpy as np


@total_ordering
class GroupScorer(GuessScorer):

    def __init__(self, guess: str, groups: list[int], possible_solutions: set):
        super().__init__(guess, groups, possible_solutions)

    def _get_comparison_key(self):
        return (len(self._groups), -np.std(self._groups), int(self._is_possible_solution))
    
    def __lt__(self, other: "GroupScorer"):
        return self._get_comparison_key() < other._get_comparison_key()
    
    def __eq__(self, other: "GroupScorer"):
        return self._get_comparison_key() == other._get_comparison_key()

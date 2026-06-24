import numpy as np


class GuessScore:

    def __init__(self, guess: str, groups: list[int], possible_solutions: set[str]):
        self._num_groups = len(groups)
        self._std = np.std(groups)
        self._is_possible_solution = guess in possible_solutions

    def _get_comparison_key(self):
        return (self._num_groups, -self._std, int(self._is_possible_solution))
    
    def __lt__(self, other: "GuessScore"):
        return self._get_comparison_key() < other._get_comparison_key()
    
    def __eq__(self, other: "GuessScore"):
        return self._get_comparison_key() == other._get_comparison_key()

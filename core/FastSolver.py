from core.Scorers.GuessScorer import GuessScorer
from core.Scorers.GroupScorer import GroupScorer
from core.Answer import Answer
from core.Solver import Solver
from core.fast_solver import calculate_guess_scores, is_accelerated


class FastSolver(Solver):
    def __init__(self, scorer: GuessScorer = GroupScorer):
        if not is_accelerated():
            raise RuntimeError(
                "Cython/OpenMP acceleration is unavailable. Run `uv sync --reinstall-package wordle` "
                "after installing python3.12-dev."
            )
        super().__init__(scorer=scorer)

    def guess(self, last_guess_answer: Answer) -> str:
        if len(self._history) == 0 and last_guess_answer is None:
            self._history.add("crane")
            return "crane"

        if last_guess_answer is not None:
            self._possible_solutions = self.filter(
                self._possible_solutions,
                last_guess_answer,
            )

        groups_by_guess = calculate_guess_scores(
            list(self.ALL_WORDS),
            self._possible_solutions,
        )

        guess_scores = {}
        for groups, guess in zip(groups_by_guess, self.ALL_WORDS):
            guess_scores[guess] = self._guess_scorer(
                guess,
                groups,
                self._possible_solutions,
            )

        best_guess = max(guess_scores, key=guess_scores.get)
        self._history.add(best_guess)

        return best_guess

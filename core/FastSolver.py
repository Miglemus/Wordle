from core.Answer import Answer
from core.Solver import Solver
from core.fast_solver import best_guess_fast, is_accelerated, openmp_threads_hint


class FastSolver(Solver):
    def __init__(self):
        if not is_accelerated():
            raise RuntimeError(
                "Cython/OpenMP acceleration is unavailable. Run `uv sync --reinstall-package wordle` "
                "after installing python3.12-dev."
            )
        super().__init__()

    def guess(self, last_guess_answer: Answer) -> str:
        if len(self._history) == 0 and last_guess_answer is None:
            self._history.add("crane")
            return "crane"

        if last_guess_answer is not None:
            self._possible_solutions = self.filter(
                self._possible_solutions,
                last_guess_answer,
            )

        print(f"Possible solutions left: {len(self._possible_solutions)}")

        best_guess, score_key = best_guess_fast(
            list(self.ALL_WORDS),
            self._possible_solutions,
        )
        self._history.add(best_guess)

        num_groups, neg_std, is_possible_solution = score_key
        print(
            f"best guess score for '{best_guess}': "
            f"GuessScore(num_groups={num_groups}, std={-neg_std:.2f}, "
            f"is_possible_solution={bool(is_possible_solution)})"
        )
        print(f"Cython/OpenMP acceleration: enabled ({openmp_threads_hint()})")
        return best_guess

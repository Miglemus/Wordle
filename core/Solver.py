from core.utils import get_all_solutions, get_all_words
from core.Answer import Answer
from core.Scorers.GuessScorer import GuessScorer
from core.Scorers.GroupScorer import GroupScorer


class Solver:
    ALL_WORDS = get_all_words()
    ALL_SOLUTIONS = get_all_solutions()

    def __init__(self, scorer: GuessScorer = GroupScorer):
        self._guess_scorer = scorer
        self._possible_solutions = set(self.ALL_SOLUTIONS)
        self._history = set()

    def guess(self, last_guess_answer: Answer) -> str:
        if len(self._history) == 0 and last_guess_answer is None:
            self._history.add("soare")
            return "soare"
 
        self._possible_solutions = self.filter(self._possible_solutions, last_guess_answer)
 
        guess_groups: dict[str, dict[Answer, int]] = {} 
        for guess in self.ALL_WORDS:
            guess_groups[guess] = {}
            for sol in self._possible_solutions:
                answer = Answer.from_guess(guess, sol)
                guess_groups[guess][answer] = guess_groups[guess].get(answer, 0) + 1

        guess_scores = {}
        for guess in self.ALL_WORDS:
            groups = list(guess_groups[guess].values())
            guess_scores[guess] = self._guess_scorer(
                guess,
                groups,
                self._possible_solutions,
            )

        best_guess = max(guess_scores, key=guess_scores.get)
        self._history.add(best_guess)
        return best_guess

    def reset(self):
        self._possible_solutions = set(self.ALL_SOLUTIONS)
        self._history = set()

    @property
    def history(self):
        return self._history

    @staticmethod
    def filter(solutions, answer: Answer):
        resulting_solutions = set()

        for sol in solutions:
            if Answer.from_guess(answer.guess, sol) == answer:
                resulting_solutions.add(sol)

        return resulting_solutions

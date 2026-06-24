from core.utils import get_all_solutions, get_all_words
from core.Answer import Answer
from core.GuessScore import GuessScore


class Solver:
    ALL_SOLUTIONS = get_all_solutions()

    def __init__(self):
        self._possible_words = get_all_words()
        self._possible_solutions = get_all_solutions()
        self._history = set()

    def guess(self, last_guess_answer: Answer) -> str:
        if len(self._history) == 0 and last_guess_answer is None:
            self._history.add("crane")
            return "crane"
 
        self._possible_solutions = self.filter(self._possible_solutions, last_guess_answer)
        self._possible_words = self.filter(self._possible_words, last_guess_answer)
 
        print(f"Possible solutions left: {len(self._possible_solutions)}")
 
        # for each guess, group up solutions with same answers
        guess_groups: dict[str, dict[Answer, int]] = {} # key-> guess, value-> dict[answer, groupsize]
        for guess in self._possible_words:
            guess_groups[guess] = {}
            for sol in self._possible_solutions:
                answer = Answer.from_guess(guess, sol)
                guess_groups[guess][answer] = guess_groups[guess].get(answer, 0) + 1

        guess_scores = {}
        for guess in self._possible_words:
            guess_scores[guess] = GuessScore(guess, list(guess_groups[guess].values()), self._possible_solutions)

        best_guess = min(guess_scores, key=guess_scores.get)
        self._history.add(best_guess)
        return best_guess

    @staticmethod
    def filter(solutions, answer: Answer):
        resulting_solutions = set()

        for sol in solutions:
            if Answer.from_guess(answer.guess, sol) == answer:
                resulting_solutions.add(sol)

        return resulting_solutions

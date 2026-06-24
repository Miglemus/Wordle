from core.utils import get_all_solutions, get_all_words
from core.Answer import Answer


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
 
        print(f"Possible solutions left: {len(self._possible_solutions)}")
 
        guesses_scores = {}
        for sol in self._possible_solutions:
            print(f"guessing for solution: {sol}")
            for guess in self._possible_solutions:
                guess_answer = Answer.from_guess(guess, sol)
                guesses_scores[guess] = guesses_scores.get(guess, 0) + len(self._possible_solutions) - len(self.filter(self._possible_solutions, guess_answer))

        best_guess = max(guesses_scores, key=guesses_scores.get) 
        self._history.add(best_guess)
        return best_guess

    @staticmethod
    def filter(solutions, answer: Answer):
        resulting_solutions = set()

        for sol in solutions:
            if Answer.from_guess(answer.guess, sol) == answer:
                resulting_solutions.add(sol)

        return resulting_solutions
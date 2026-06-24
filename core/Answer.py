from enum import Enum

class Result(Enum):
    CORRECT = "correct"
    PRESENT = "present"
    ABSENT = "absent"


class Answer:

    def __init__(self, result: list[Result] = None, guess: str = None):
        self._result: list[Result] = result if result is not None else []
        self._guess: str = guess

    @property
    def result(self):
        return self._result
    
    @property
    def guess(self):
        return self._guess

    @classmethod
    def from_guess(cls, guess: str, solution: str) -> "Answer":
        result: list[Result] = [Result.ABSENT] * len(guess)
        solution_letters = list(solution)
        
        for i, (g_char, s_char) in enumerate(zip(guess, solution)):
            if g_char == s_char:
                result[i] = Result.CORRECT
                solution_letters[i] = None 

        for i, g_char in enumerate(guess):
            if result[i] == Result.CORRECT:
                continue
 
            if g_char in solution_letters:
                result[i] = Result.PRESENT
                idx = solution_letters.index(g_char)
                solution_letters[idx] = None
            else:
                result[i] = Result.ABSENT

        return cls(result, guess)

    def is_correct(self) -> bool:
        return all(r == Result.CORRECT for r in self._result)

    def __eq__(self, other: "Answer"):
        return self._result == other.result

    def __ne__(self, other: "Answer"):
        return not self.__eq__(other)

    def __str__(self) -> str:
        # return emojis (squares) for each result
        # 🟩 for correct, 🟨 for present, ⬛ for absent
        result_str = ""
        for r in self._result:
            if r == Result.CORRECT:
                result_str += "🟩"
            elif r == Result.PRESENT:
                result_str += "🟨"
            else:
                result_str += "⬛"
        return result_str

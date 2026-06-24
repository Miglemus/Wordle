

class Answer:

    def __call__(self, guess: str, solution: str) -> list[str]:
        result = []
        for g_char, s_char in zip(guess, solution):
            if g_char == s_char:
                result.append("correct")
            elif g_char in solution:
                result.append("present")
            else:
                result.append("absent")
        return result
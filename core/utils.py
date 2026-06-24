SOLUTION_FILE = "solutions.txt"
GUESSES_FILE = "wordle-guesses.txt"

def get_all_solutions() -> set[str]:
    with open(SOLUTION_FILE, "r") as f:
        solutions = f.readlines()
    
    return {solution.strip().lower() for solution in solutions}
    
def get_all_guesses() -> set[str]:
    with open(GUESSES_FILE, "r") as f:
        guesses = f.readlines()
    
    return {guess.strip().lower() for guess in guesses}

def get_all_words() -> set[str]:
    return get_all_solutions().union(get_all_guesses())
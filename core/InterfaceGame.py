from core.Interface import Interface
from core.Game import Game


class InterfaceGame(Interface):
    def __init__(self, game: Game):
        self._game = game

    def play(self):
        print("Welcome to Wordle!")
        print("You have 6 attempts to guess the 5-letter word.")
        print("After each guess, you'll receive feedback on your guess.")
        print("Let's begin!\n")

        attempts = 6
        for attempt in range(attempts):
            guess = input(f"Attempt {attempt + 1}/{attempts}: ").strip().lower()
            if len(guess) != 5:
                print("Please enter a 5-letter word.")
                continue

            result = self._game.step(guess)
            print(result)

            if result.is_correct():
                print(f"Congratulations! You've guessed the word '{self._game._solution}' correctly!")
                break
        else:
            print(f"Sorry, you've used all attempts. The correct word was '{self._game._solution}'.")

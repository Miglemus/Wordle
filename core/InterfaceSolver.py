import io
from contextlib import redirect_stdout

from core.Answer import Answer
from core.Interface import Interface
from core.Solver import Solver
from core.ui_components import (
    GuessRow,
    celebration_panel,
    feedback_help,
    game_layout,
    result_from_feedback_char,
    title_panel,
    wordle_grid,
)
from rich.console import Console


class InterfaceSolver(Interface):

    def __init__(self, solver: Solver):
        self._solver = solver
        self._console = Console()
        self._rows: list[GuessRow] = []

    def play(self):
        self._console.clear()
        self._console.print(title_panel("WORDLE SOLVER", "Pensez a un mot, puis guidez l'IA avec les couleurs."))
        guess = self._guess(None)

        while True:
            answer = self._ask_answer(guess)
            self._rows.append(GuessRow(guess, answer))

            if answer.is_correct():
                self._console.print(
                    celebration_panel(
                        "Resolution terminee",
                        f"L'IA a trouve {guess.upper()} en {len(self._rows)} essai(s).",
                        self._rows,
                    )
                )
                return

            guess = self._guess(answer)
            self._console.print(
                game_layout(
                    "Mode solver",
                    self._rows,
                    solutions_left=self._solutions_left(),
                    possible_words=self._possible_words(),
                )
            )

    def _guess(self, answer: Answer | None) -> str:
        with redirect_stdout(io.StringIO()):
            return self._solver.guess(answer)

    def _ask_answer(self, guess: str) -> Answer:
        while True:
            self._console.print(
                game_layout(
                    "Mode solver",
                    self._rows,
                    f"Mot propose : [bold]{guess.upper()}[/bold]",
                    solutions_left=self._solutions_left(),
                    possible_words=self._possible_words(),
                )
            )
            self._console.print(wordle_grid([], current_guess=guess, max_attempts=1))
            feedback = self._console.input(f"[bold]Retour couleur[/bold] ({feedback_help()}) > ").strip()
            try:
                if len(feedback) != 5:
                    raise ValueError("Feedback must contain 5 characters.")
                return Answer([result_from_feedback_char(char) for char in feedback], guess)
            except ValueError:
                self._console.print("[bold red]Retour invalide. Utilisez exactement 5 caracteres : v, j ou g.[/bold red]")

    def _solutions_left(self) -> int:
        return len(self._solver._possible_solutions)

    def _possible_words(self) -> set[str]:
        return self._solver._possible_solutions

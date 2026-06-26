import io
import time
from time import perf_counter
from contextlib import redirect_stdout

from core.Interface import Interface
from core.Game import Game
from core.Solver import Solver
from core.Answer import Answer
from core.timing import format_duration
from core.ui_components import GuessRow, celebration_panel, game_layout, title_panel
from rich.console import Console
from rich.live import Live


class InterfaceGameSolver(Interface):
    
    def __init__(self, game: Game, solver: Solver):
        self._game = game
        self._solver = solver
        self._console = Console()
        self._rows: list[GuessRow] = []
        self._last_guess_duration = 0.0

    def run(self):
        self._console.clear()
        self._console.print(title_panel("AUTO SOLVER", "Observez l'IA resoudre la grille en temps reel."))

        answer = None
        guess = ""
        with Live(
            game_layout(
                "Mode auto",
                self._rows,
                solutions_left=self._solutions_left(),
                possible_words=self._possible_words(),
            ),
            console=self._console,
            refresh_per_second=8,
        ) as live:
            while not self._game.is_over and len(self._rows) < 6:
                guess = self._guess(answer)
                live.update(
                    game_layout(
                        "Mode auto",
                        self._rows,
                        f"L'IA tente [bold]{guess.upper()}[/bold].\n"
                        f"Temps de calcul : [bold cyan]{format_duration(self._last_guess_duration)}[/bold cyan]",
                        solutions_left=self._solutions_left(),
                        possible_words=self._possible_words(),
                    )
                )
                time.sleep(0.6)

                partial = ""
                for letter in guess:
                    partial += letter
                    live.update(
                        game_layout(
                            "Mode auto",
                            self._rows,
                            f"Lecture de {guess.upper()}...",
                            solutions_left=self._solutions_left(),
                            possible_words=self._possible_words(),
                            current_guess=partial,
                        )
                    )
                    time.sleep(0.12)

                answer = self._game.step(guess)
                self._solver._possible_solutions = self._solver.filter(self._solver._possible_solutions, answer)
                for index in range(1, len(guess) + 1):
                    partial_answer = Answer(answer.result[:index], guess[:index])
                    live.update(
                        game_layout(
                            "Mode auto",
                            self._rows,
                            f"Evaluation de {guess.upper()}...",
                            solutions_left=self._solutions_left(),
                            possible_words=self._possible_words(),
                            current_guess=guess,
                            current_answer=partial_answer,
                        )
                    )
                    time.sleep(0.12)

                self._rows.append(GuessRow(guess, answer))
                live.update(
                    game_layout(
                        "Mode auto",
                        self._rows,
                        solutions_left=self._solutions_left(),
                        possible_words=self._possible_words(),
                    )
                )
                time.sleep(0.6)

        self._console.print(
            celebration_panel(
                "Resolution terminee",
                f"L'IA a trouve {guess.upper()} en {len(self._rows)} essai(s).",
                self._rows,
            )
        )

    def _guess(self, answer: Answer | None) -> str:
        start = perf_counter()
        with redirect_stdout(io.StringIO()):
            guess = self._solver.guess(answer)
        self._last_guess_duration = perf_counter() - start
        return guess

    def _solutions_left(self) -> int:
        return len(self._solver._possible_solutions)

    def _possible_words(self) -> set[str]:
        return self._solver._possible_solutions

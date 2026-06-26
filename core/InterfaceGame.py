import io
from time import perf_counter
from contextlib import redirect_stdout

from core.Interface import Interface
from core.Game import Game
from core.Solver import Solver
from core.timing import format_duration
from core.ui_components import GuessRow, celebration_panel, game_layout, title_panel
from core.utils import get_all_words
from rich.console import Console


class InterfaceGame(Interface):
    def __init__(self, game: Game, solver: Solver):
        self._game = game
        self._solver = solver
        self._console = Console()
        self._rows: list[GuessRow] = []
        self._synced_hint_rows = 0
        self._last_hint = ""
        self._last_hint_duration = 0.0

    def run(self):
        self._console.clear()
        self._console.print(title_panel("WORDLE", "Devinez le mot en 6 essais. Tapez hint pour recevoir une aide."))
        attempts = 6

        while len(self._rows) < attempts and not self._game.is_over:
            self._console.print(game_layout("Mode joueur", self._rows))
            guess = self._console.input(f"[bold]Essai {len(self._rows) + 1}/{attempts}[/bold] > ").strip().lower()

            if guess == "hint":
                self._console.print(
                    game_layout(
                        "Mode joueur",
                        self._rows,
                        self._hint_message(),
                        solutions_left=self._solutions_left(),
                        possible_words=self._possible_words(),
                    )
                )
                continue

            if not self._is_valid_guess(guess):
                self._console.print("[bold red]Mot invalide. Entrez un mot de 5 lettres du dictionnaire officiel.[/bold red]")
                continue

            result = self._game.step(guess)
            self._rows.append(GuessRow(guess, result))

            if result.is_correct():
                self._console.print(
                    celebration_panel(
                        "Victoire",
                        f"Bravo, vous avez trouve {self._game._solution.upper()} en {len(self._rows)} essai(s).",
                        self._rows,
                    )
                )
                return

        self._console.print(
            celebration_panel(
                "Partie terminee",
                f"Le mot etait {self._game._solution.upper()}. Belle tentative.",
                self._rows,
            )
        )

    def _is_valid_guess(self, guess: str) -> bool:
        return len(guess) == 5 and guess.isalpha() and guess in get_all_words()

    def _hint_message(self) -> str:
        if not self._rows:
            if not self._last_hint:
                self._last_hint = self._timed_guess(None)
            return (
                "[italic cyan]Suggestion strategique : CRANE.[/italic cyan]\n"
                f"Temps de calcul : [bold cyan]{format_duration(self._last_hint_duration)}[/bold cyan]"
            )

        self._sync_hint_solver()
        suggestions = []
        best_guess = self._last_hint

        suggestions.append(best_guess.upper())
        for word in sorted(self._solver._possible_solutions):
            candidate = word.upper()
            if candidate not in suggestions:
                suggestions.append(candidate)
            if len(suggestions) == 3:
                break

        if len(suggestions) == 1:
            suggestion_text = suggestions[0]
        else:
            suggestion_text = f"{', '.join(suggestions[:-1])} ou {suggestions[-1]}"

        return (
            f"[italic cyan]Besoin d'un coup de main ? Essayez {suggestion_text}.[/italic cyan]\n"
            f"Temps de calcul : [bold cyan]{format_duration(self._last_hint_duration)}[/bold cyan]"
        )

    def _sync_hint_solver(self) -> None:
        if not self._solver._history:
            self._last_hint = self._timed_guess(None)
        for row in self._rows[self._synced_hint_rows:]:
            self._last_hint = self._timed_guess(row.answer)
            self._synced_hint_rows += 1

    def _timed_guess(self, answer):
        start = perf_counter()
        with redirect_stdout(io.StringIO()):
            guess = self._solver.guess(answer)
        self._last_hint_duration = perf_counter() - start
        return guess

    def _solutions_left(self) -> int:
        return len(self._solver._possible_solutions)

    def _possible_words(self) -> set[str]:
        return self._solver._possible_solutions

from __future__ import annotations

from dataclasses import dataclass

from rich import box
from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.Answer import Answer, Result


RESULT_STYLES = {
    Result.CORRECT: "bold white on #6aaa64",
    Result.PRESENT: "bold white on #c9b458",
    Result.ABSENT: "bold white on #787c7e",
}
UNKNOWN_STYLE = "bold white on #121213"
UNKNOWN_BORDER = "#3a3a3c"
KEYBOARD_ROWS = ("qwertyuiop", "asdfghjkl", "zxcvbnm")
RESULT_RANK = {
    Result.ABSENT: 1,
    Result.PRESENT: 2,
    Result.CORRECT: 3,
}


@dataclass(frozen=True)
class GuessRow:
    guess: str
    answer: Answer


def result_from_feedback_char(char: str) -> Result:
    normalized = char.lower()
    if normalized in {"v", "c"}:
        return Result.CORRECT
    if normalized in {"j", "p"}:
        return Result.PRESENT
    if normalized in {"g", "a"}:
        return Result.ABSENT
    raise ValueError(f"Invalid feedback character: {char}")


def feedback_help() -> str:
    return "v/c = vert, j/p = jaune, g/a = gris"


def wordle_tile(letter: str = "", result: Result | None = None) -> Panel:
    label = Text(letter.upper(), justify="center", style="bold white")
    style = RESULT_STYLES.get(result, UNKNOWN_STYLE)
    border_style = style if result is not None else UNKNOWN_BORDER
    return Panel(
        Align.center(label, vertical="middle"),
        box=box.SQUARE,
        style=style,
        border_style=border_style,
        width=5,
        height=3,
        padding=(0, 1),
    )


def wordle_row(guess: str = "", answer: Answer | None = None) -> Table:
    table = Table.grid(padding=(0, 1))
    for _ in range(5):
        table.add_column(width=7)

    letters = guess[:5].ljust(5)
    results = (answer.result + [None] * 5)[:5] if answer is not None else [None] * 5
    table.add_row(*(wordle_tile(letter.strip(), result) for letter, result in zip(letters, results)))
    return table


def wordle_grid(rows: list[GuessRow], current_guess: str = "", max_attempts: int = 6) -> Group:
    rendered_rows = [wordle_row(row.guess, row.answer) for row in rows]
    if len(rendered_rows) < max_attempts and current_guess:
        rendered_rows.append(wordle_row(current_guess))
    while len(rendered_rows) < max_attempts:
        rendered_rows.append(wordle_row())
    return Group(*rendered_rows[:max_attempts])


def keyboard_state(rows: list[GuessRow]) -> dict[str, Result]:
    state: dict[str, Result] = {}
    for row in rows:
        for letter, result in zip(row.guess, row.answer.result):
            previous = state.get(letter)
            if previous is None or RESULT_RANK[result] > RESULT_RANK[previous]:
                state[letter] = result
    return state


def virtual_keyboard(rows: list[GuessRow]) -> Panel:
    state = keyboard_state(rows)
    rendered_rows = []
    for letters in KEYBOARD_ROWS:
        line = Text(justify="center")
        for letter in letters:
            result = state.get(letter)
            style = RESULT_STYLES.get(result, "bold white on #3a3a3c")
            line.append(f"{letter.upper()} ", style=style)
        rendered_rows.append(Align.center(line))
    return Panel(Group(*rendered_rows), title="Clavier", border_style="#565758", box=box.ROUNDED)


def title_panel(title: str, subtitle: str) -> Panel:
    content = Group(
        Align.center(Text(title, style="bold #6aaa64")),
        Align.center(Text(subtitle, style="italic #d7dadc")),
    )
    return Panel(content, border_style="#6aaa64", box=box.DOUBLE)


def game_layout(
    title: str,
    rows: list[GuessRow],
    message: str = "",
    solutions_left: int | None = None,
    possible_words: set[str] | None = None,
    current_guess: str = "",
    current_answer: Answer | None = None,
) -> Panel:
    side_lines = [virtual_keyboard(rows)]
    if solutions_left is not None:
        side_lines.append(Panel(f"[bold green]Solutions restantes : {solutions_left}[/bold green]", border_style="green"))
    if possible_words is not None and 0 < len(possible_words) < 10:
        words = ", ".join(word.upper() for word in sorted(possible_words))
        side_lines.append(Panel(words, title="Mots possibles", border_style="#6aaa64"))
    if message:
        side_lines.append(Panel(message, border_style="#c9b458"))

    grid_rows = rows
    grid_current = current_guess
    if current_answer is not None:
        grid_rows = rows + [GuessRow(current_guess, current_answer)]
        grid_current = ""

    table = Table.grid(expand=True)
    table.add_column(ratio=3)
    table.add_column(ratio=2)
    table.add_row(Align.center(wordle_grid(grid_rows, current_guess=grid_current)), Group(*side_lines))
    return Panel(table, title=title, border_style="#6aaa64", box=box.ROUNDED)


def celebration_panel(title: str, body: str, rows: list[GuessRow]) -> Panel:
    return Panel(
        Group(Align.center(wordle_grid(rows)), Align.center(Text(body, style="bold white"))),
        title=title,
        border_style="#6aaa64",
        box=box.DOUBLE,
    )

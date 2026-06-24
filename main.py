from core.Game import Game
import tyro
from tyro.conf import arg
from dataclasses import dataclass
from typing import List, Annotated


@dataclass
class CLI:
    solution: Annotated[bool, arg(help="Print the solution")] = False
    solve: Annotated[bool, arg(help="Solve the game")] = False

if __name__ == "__main__":
    args = tyro.cli(CLI)
    game = Game()

    print(game.solution)

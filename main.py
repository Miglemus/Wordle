from core.Game import Game
import tyro
from dataclasses import dataclass
from typing import Literal, Annotated
from core.InterfaceGameSolver import InterfaceGameSolver
from core.InterfaceSolver import InterfaceSolver
from core.InterfaceGame import InterfaceGame
from core.Solver import Solver


@dataclass
class CLI:
    game_mode: Annotated[Literal["solver", "game_solver", "game"], tyro.conf.arg(aliases=["-g"])] = "solver"

if __name__ == "__main__":
    args = tyro.cli(CLI)

    if args.game_mode == "solver":
        interface = InterfaceSolver(solver=Solver())
    elif args.game_mode == "game_solver":
        game = Game()
        interface = InterfaceGameSolver(game=game, solver=Solver())
    elif args.game_mode == "game":
        game = Game()
        interface = InterfaceGame(game=game)

    if hasattr(interface, "_game"):
        print(f"Solution: {interface._game._solution}")
    interface.play()

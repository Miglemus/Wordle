from core.Game import Game
import tyro
from dataclasses import dataclass
from typing import Literal, Annotated
from core.InterfaceGameSolver import InterfaceGameSolver
from core.InterfaceSolver import InterfaceSolver
from core.InterfaceGame import InterfaceGame
from core.Solver import Solver
from core.FastSolver import FastSolver
from core.Scorers.GroupScorer import GroupScorer
from core.Scorers.StdScorer import StdScorer
from core.Scorers.EntropyScorer import EntropyScorer
from core.Benchmark import Benchmark


@dataclass
class CLI:
    game_mode: Annotated[Literal["solver", "game_solver", "game", "benchmark"], tyro.conf.arg(aliases=["-g"])] = "solver"
    solver: Annotated[Literal["normal", "fast"], tyro.conf.arg(aliases=["-s"])] = "normal"
    scorer: Annotated[Literal["group", "std", "entropy"], tyro.conf.arg(aliases=["-c"])] = "group"

if __name__ == "__main__":
    args = tyro.cli(CLI)

    scorer = GroupScorer if args.scorer == "group" else StdScorer if args.scorer == "std" else EntropyScorer

    if args.game_mode == "solver":
        solver = FastSolver(scorer=scorer) if args.solver == "fast" else Solver(scorer=scorer)
        interface = InterfaceSolver(solver=solver)
    elif args.game_mode == "game_solver":
        solver = FastSolver(scorer=scorer) if args.solver == "fast" else Solver(scorer=scorer)
        game = Game()
        interface = InterfaceGameSolver(game=game, solver=solver)
    elif args.game_mode == "game":
        solver = FastSolver(scorer=scorer) if args.solver == "fast" else Solver(scorer=scorer)
        game = Game()
        interface = InterfaceGame(game=game, solver=solver)
    elif args.game_mode == "benchmark":
        solver = FastSolver(scorer=scorer) if args.solver == "fast" else Solver(scorer=scorer)
        game = Game()
        interface = Benchmark(game=game, solver=solver)

    if hasattr(interface, "_game"):
        print(f"Solution: {interface._game._solution}")
    interface.run()

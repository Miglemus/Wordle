from core.Interface import Interface
from core.Game import Game
from core.Solver import Solver


class InterfaceSolver(Interface):

    def __init__(self, solver: Solver):
        self._solver = solver

    def play(self):
        pass
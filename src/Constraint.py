import numpy as np
from src.Variable import Variable
from src.AC3 import AC3
import abc


class Constraint:
    # x,y: Variable, type: char
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

    # x: Variable
    @abc.abstractmethod
    def filter_from(self, x):
        # applying filtering alg
        pass
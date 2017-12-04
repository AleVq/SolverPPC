from src.Constraint import Constraint
from src.Variable import Variable
from src.Propagation import Propagation
import numpy as np


def consistent(x, y, type):
    if type == '!=':
        return x != y
    elif type == '<':
        return x < y
    elif type == '>':
        return x > y


def initialize(constraints):
    q = []
    s = []
    for arc in constraints:
        for v in arc.x.domain:
            total = 0
            for w in arc.y.domain:
                if consistent(v, w, arc.type):
                    total += 1


def revise(x, y, type):
    deleted = False
    for v in x.domain:
        consistent_value = False
        for w in y.domain:
            if consistent(v, w, type):
                consistent_value = True
                break
        if not consistent_value:
            x.remove_value(v)
            deleted = True
    return deleted


class ArcConsistencyAlgorithms:

    def filter_from(self, x):
        # applying filtering alg
        if x.is_delta_empty():
            return False

    # vars, constraints: numpy array
    def ac3(variables, constraints, prop):
        for c in constraints:
            prop.add_to_queue(c)
        while not prop.queue.is_empty():
            c = prop.pick_in_queue()
            if revise(c.x, c.y, c.type):
                for c1 in constraints:
                    if c1.y.name == c.x.name:
                        prop.queue.enqueue(c1)
        return variables

    # vars, constraints: numpy array
   # def ac4(variables, constraints, prop):
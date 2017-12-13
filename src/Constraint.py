import numpy as np
import abc


def consistent(x, y, expr):
    return eval(expr)


# x,y: Variable, type: String
def make_table(x, y, type):
    result = np.zeros((x.domain.shape[0], y.domain.shape[0]))
    for i in range(x.domain.shape[0]):
        for j in range(y.domain.shape[0]):
            if consistent(x.domain[i], y.domain[j], type):
                result[i, j] = 1
    return result


class Constraint:
    # x,y: Variable, type: char
    def __init__(self, x, y, type, table=None):
        self.table = table
        if self.table is None:
            self.table = make_table(x, y, type)
        self.x = x
        self.y = y
        self.type = type

    # x: Variable
    @abc.abstractmethod
    def filter_from(self, x):
        # applying filtering alg
        pass
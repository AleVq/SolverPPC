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

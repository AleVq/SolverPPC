from src.Constraint import Constraint
from src.Variable import Variable
from src.Propagation import Propagation
from src.AC import AC3
import numpy as np


def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)


class Model:

    def __init__(self):
        self.variables = np.array([])
        self.constraints = np.array([])
        self.propagation = Propagation()

    # domain, delta: list
    def add_var(self, domain):
        self.variables = np.append(self.variables, Variable('x'+str(self.variables.shape[0]), np.array(domain), self.propagation))
        return self.variables[self.variables.shape[0]-1]

    # x, y: Variable, type: String
    def add_constr(self, x, y, type):
        self.constraints = np.append(self.constraints, AC3(x, y, type))
        self.propagation.update_constraints_graph(self.constraints[self.constraints.shape[0]-1])

    def get_var(self, name):
        return self.variables[int(name[1])]

    def find_solution(self):
        return self.backtrack([], self.variables, self.constraints)

    # lab: list, unlab, cons: np array
    # lab = vars with fixed value
    def backtrack(self, lab, unlab, cons):  # unlab = queue of Regin's propagation, lab = fixed-valued vars
        if unlab.shape[0] == 0:
            return lab
        x = unlab[0]
        # iterate over all values of x
        for v in x.domain:
            # domain = x.domain
            x.domain = np.array([v])
            self.filter_all()
            new_lab = lab.copy()
            new_lab.append(x)
            result = self.backtrack(new_lab, np.delete(unlab, 0), cons)
            # x.domain = np.setdiff1d(domain, v)
            if len(result) != 0:
                return result
        return []  # all values are inconsistent, must go back

    def filter_all(self):
        self.propagation.run(self.variables)
        return self.variables


if __name__ == '__main__':
    m = Model()
    x0 = m.add_var(list(range(1,14)))
    x1 = m.add_var(list(range(5,16)))
    x2 = m.add_var(list(range(11,16)))
    x3 = m.add_var(list(range(5,25)))
    m.add_constr(x0, x1, '<')
    m.add_constr(x1, x2, '>')
    m.add_constr(x2, x3, '<')
    m.add_constr(x0, x3, '>')
    vars_domain = m.filter_all()
    for var in vars_domain:
        print(str(var.name) + "'s domain: " + str(var.domain))
    vars_sol = m.find_solution()
    for var in vars_sol:
        print(str(var.name) + "'s value: " + str(var.domain))

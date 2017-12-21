from src.Variable import Variable
from src.Propagation import Propagation
from src.AC import AC3
from src.AC import AC4
from src.AC import AC6
from src.AC import AC2001
import numpy as np
from src.Propagation import Queue
import time


def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)


class Model:

    def __init__(self, alg_ac):
        self.variables = np.array([])
        self.constraints = np.array([])
        self.propagation = Propagation()
        self.alg_ac = alg_ac

    # domain: list
    def add_var(self, domain):
        self.variables = np.append(self.variables, Variable('x'+str(self.variables.shape[0]), np.array(domain), self.propagation))
        return self.variables[self.variables.shape[0]-1]

    # x, y: Variable, type: String
    def add_constr(self, x, y, type):
        if self.alg_ac == 3:
            self.constraints = np.append(self.constraints, AC3(x, y, type))
        elif self.alg_ac == 4:
            self.constraints = np.append(self.constraints, AC4(x, y, type))
        elif self.alg_ac == 6:
            self.constraints = np.append(self.constraints, AC6(x, y, type))
        elif self.alg_ac == 2001:
            self.constraints = np.append(self.constraints, AC2001(x, y, type))
        self.propagation.update_constraints_graph(self.constraints[self.constraints.shape[0]-1])

    # returns first solution found by using backtracking
    def find_solution(self):
        if self.variables.shape[0] < 2:
            print('Minimum number of variables: 2')
            return False
        q = Queue()
        q.enqueue(self.variables)
        start = time.time()
        result = self.backtrack()
        end = time.time()
        if result == []:
            print('No feasible solution with AC' + str(self.alg_ac))
        else:
            print('Solution with AC' + str(self.alg_ac) + ': ' + str([item.domain[0] for item in self.variables])
                  + ', computed in ' + str("{0:.3f}".format(end-start)) + ' seconds')
        return end-start

    def all_labelled(self):
        res = 0
        for var in self.variables:
            res += var.label
        return res == self.variables.shape[0]

    # lab: list, unlab, cons: np array
    # lab = vars with fixed value, unlab = vars in queue, cons = constraints
    def backtrack(self):
        if self.all_labelled():
            return self.variables
        x = self.variables[0]
        for var in self.variables:
            if not var.label:
                x = var
                var.label = True
                break
        domain = x.domain
        for v in domain:
            bp = []  # backup of actual state of vars
            for variable in self.variables:
                bp.append(variable.domain)
            x.domain = np.array([v])
            x.delta = np.setdiff1d(domain, [v])
            if self.alg_ac != 3:
                for c in self.constraints:
                    c.initialize()
            feasible = self.filter_all()
            if feasible:
                result = self.backtrack()
                if len(result) != 0:
                    return result
            for i in range(self.variables.shape[0]):
                self.variables[i].domain = bp[i]
                self.variables[i].reset_delta()
                if var.name == x.name:
                    var.label = False
            if self.alg_ac != 3:
                for c in self.constraints:
                    c.initialize()
        return []  # all values are inconsistent, must go back

    def print_filtered_domains(self):
            self.propagation.run(self.variables)  # (vars)
            print('Filtered domains:')
            for var in self.variables:
                print(str(var.name) + "'s domain: " + str(var.domain))

    def filter_all(self):
        if self.variables.shape[0] < 2:
            print('Minimum number of variables: 2')
            return False
        return self.propagation.run(self.variables)

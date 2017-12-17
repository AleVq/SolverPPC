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

    # domain, delta: list
    def add_var(self, domain):
        self.variables = np.append(self.variables, Variable('x'+str(self.variables.shape[0]), np.array(domain), self.propagation))
        return self.variables[self.variables.shape[0]-1]

    # x, y: Variable, type: String
    def add_constr(self, x, y, type):
        if m.alg_ac == 3:
            self.constraints = np.append(self.constraints, AC3(x, y, type))
        elif m.alg_ac == 4:
            self.constraints = np.append(self.constraints, AC4(x, y, type))
        elif self.alg_ac == 6:
            self.constraints = np.append(self.constraints, AC6(x, y, type))
        elif self.alg_ac == 2001:
            self.constraints = np.append(self.constraints, AC2001(x, y, type))
        self.propagation.update_constraints_graph(self.constraints[self.constraints.shape[0]-1])

    def get_var(self, name):
        return self.variables[int(name[1])]

    def find_solution(self):
        q = Queue()
        q.enqueue(self.variables)
        start = time.time()
        result = self.backtrack()
        end = time.time()
        print('Time to find solution with backtrack: ' + str(end - start) + ' seconds.')
        if result == []:
            print('No feasible solution')
        else:
            for variables in result:
                print(str(variables.name) + " = " + str(variables.domain))

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
        return self.propagation.run(self.variables)


if __name__ == '__main__':
    for x in [3, 4, 6, 2001]:
        print('AC' + str(x) + ':')
        m = Model(x)
        # vars and constraints for n-queens problem
        n = 8
        for i in range(n):
            m.add_var(list(range(n)))
        for i in range((n-1)):
            for j in range((i+1), n):
                a = j-i
                m.add_constr(m.variables[i], m.variables[j], "x != y and x != (y-" +str(a) + ')' + " and x != (y+"+str(a) + ')')
        m.print_filtered_domains()
        m.find_solution()
from src.Variable import Variable
from src.Propagation import Propagation
from src.AC import AC3
from src.AC import AC4
from src.AC import AC6
from src.AC import AC2001
import numpy as np
from src.Propagation import Queue
from src.Constraint import Constraint


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

    def createConstraint(self, x, y, type):
        if m.alg_ac == 3:
            return AC3(x, y, type)
        elif m.alg_ac == 4:
            return AC4(x, y, type)
        elif self.alg_ac == 6:
            return AC6(x, y, type)
        elif self.alg_ac == 2001:
            return AC2001(x, y, type)

    def get_var(self, name):
        return self.variables[int(name[1])]

    def find_solution(self):
        q = Queue()
        q.enqueue(self.variables)
        return self.backtrack()

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
            #for value in self.variables:
            #   print(str(value.name) + ' ' + str(value.domain))
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

    def filter_all(self, cons=None):
            return self.propagation.run(self.variables)  # (vars)


if __name__ == '__main__':
    for x in [3, 4, 6, 2001]:
        print('AC' + str(x) + ':')
        m = Model(x)
        switch_csp = 9
        if switch_csp == 0:
            x0 = m.add_var(list(range(1,14)))
            x1 = m.add_var(list(range(5,16)))
            x2 = m.add_var(list(range(11,16)))
            x3 = m.add_var(list(range(5,25)))
            m.add_constr(x0, x1, 'x < (y-4)')
            m.add_constr(x1, x2, 'x > y')
            m.add_constr(x2, x3, 'x < y')
            m.add_constr(x0, x3, 'x != y')
        elif switch_csp == 2:
            x0 = m.add_var(list(range(0,4)))
            x1 = m.add_var(list(range(0,4)))
            m.add_constr(x0, x1, 'x+y > 4')
        else:
            n = 8
            for i in range(n):
                m.add_var(list(range(n)))
            for i in range((n-1)):
                for j in range((i+1), n):
                    a = j-i
                    m.add_constr(m.variables[i], m.variables[j], "x != y and x != (y-" +str(a) + ')' + " and x != (y+"+str(a) + ')')
                    #m.add_constr(m.variables[i], m.variables[j], "x != (y-"+str(a) + ')')
                    #m.add_constr(m.variables[i], m.variables[j], "x != (y+"+str(a) + ')')

        #m.filter_all()
        #vars_domain = m.variables
        #print('Filtered domains:')
        #for var in vars_domain:
        #    print(str(var.name) + "'s domain: " + str(var.domain))
        vars_sol = m.find_solution()
        print('Proposed solution:')
        for var in vars_sol:
            print(str(var.name) + " = " + str(var.domain))


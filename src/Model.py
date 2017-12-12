from src.Constraint import Constraint
from src.Variable import Variable
from src.Propagation import Propagation
from src.AC import AC3
from src.AC import AC4
from src.AC import AC6
import numpy as np
from src.Propagation import Queue
from src.AC import consistent


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
        self.propagation.update_constraints_graph(self.constraints[self.constraints.shape[0]-1])

    def get_var(self, name):
        return self.variables[int(name[1])]

    def find_solution(self):
        q = Queue()
        q.enqueue(self.variables)
        return self.backtrack([], self.variables)


    # lab: list, unlab, cons: np array
    # lab = vars with fixed value, unlab = vars in queue, cons = constraints
    def backtrack(self, lab, unlab):
        if unlab.shape[0] == 0:
            return lab
        x = unlab[0]
        domain = x.domain
        for v in domain:
            x.domain = np.array([v])
            backup_vars = self.variables
            for var in lab:
                print(str(var.name) + ' domain: ' + str(var.domain))
            if self.filter_all():
                new_lab = lab.copy()
                new_lab.append(x)
                result = self.backtrack(new_lab, np.delete(unlab, 0))
    #            result = self.backtrack(new_lab, np.delete(unlab, 0), cons)
                if len(result) != 0:
                    return result
            else:
                self.variables = backup_vars
        return []  # all values are inconsistent, must go back

    def lab_cons(self, v, x, lab, cons):
        for c in cons:
            if c.x.name == x.name and c.y in lab and not consistent(v, c.y.domain[0], c.type):
                return False
            elif c.y.name == x.name and c.x in lab and not consistent(c.x.domain[0], v, c.type):
                return False
        return True

    def filter_all(self):
        vars = [item for item in self.variables if not item.is_delta_empty()]
        return self.propagation.run(self.variables)  # (vars)



if __name__ == '__main__':
    for x in [3,4,6]:
        print('AC' + str(x) + ':')
        m = Model(x)
        x0 = m.add_var(list(range(1,14)))
        x1 = m.add_var(list(range(5,16)))
        x2 = m.add_var(list(range(11,16)))
        x3 = m.add_var(list(range(5,25)))
        m.add_constr(x0, x1, 'x < (y-4)')
        m.add_constr(x1, x2, 'x > y')
        m.add_constr(x2, x3, 'x < y')
        m.add_constr(x0, x3, 'x != y')
        '''
        n = 8
        for i in range(n):
            m.add_var(list(range(n)))
        for i in range((n-1)):
            for j in range((i+1), n):
                a = j-i
                m.add_constr(m.variables[i], m.variables[j], "x != y")
                m.add_constr(m.variables[i], m.variables[j], "x != (y-"+str(a) + ')')
                m.add_constr(m.variables[i], m.variables[j], "x != (y+"+str(a) + ')')
        '''
        m.filter_all()
        vars_domain = m.variables
        print('Filtered domains:')
        for var in vars_domain:
            print(str(var.name) + "'s domain: " + str(var.domain))
        #vars_sol = m.find_solution()
        #print('Proposed solution:')
        #for var in vars_sol:
        #    print(str(var.name) + " = " + str(var.domain))

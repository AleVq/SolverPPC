from src.Constraint import Constraint
from src.Variable import Variable
from src.Propagation import Propagation
from src.AC3 import AC3
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
    def add_var(self, name, domain):
        self.variables = np.append(self.variables, Variable(name, np.array(domain), self.propagation))

    # x, y: Variable, type: String
    def add_constr(self, x, y, type):
        self.constraints = np.append(self.constraints, Constraint(x, y, type))
        self.propagation.update_constraints_graph(self.constraints[self.constraints.shape[0]-1])

    def get_var(self, name):
        return self.variables[int(name[1])]

    def arc_consistency(self, alg):
        if alg == '3':
            ac3 = AC3()
            prop = Propagation()
            self.variables = prop.run(self.variables, self.constraints, self.propagation)
        # elif alg == '4':
        #    self.variables = AC4.ac4(self.variables, self.constraints, self.propagation)
        #for var in self.variables:
        #    print(str(var.name) + "'s domain: " + str(var.domain))


if __name__ == '__main__':
    m = Model()
    m.add_var('x'+str(0), list(range(1,14)))
    m.add_var('x'+str(1), list(range(5,16)))
    m.add_var('x'+str(2), list(range(11,16)))
    m.add_var('x'+str(3), list(range(5,65)))
    '''
    m.add_var('x'+str(0), list(char_range('a','e')))
    m.add_var('x'+str(1), list(char_range('d','p')))
    m.add_var('x'+str(2), list(char_range('k','t')))
    m.add_var('x'+str(3), list(char_range('n','z')))
    '''
    x = m.get_var('x0')
    y = m.get_var('x1')
    z = m.get_var('x2')
    t = m.get_var('x3')
    m.add_constr(x, y, '>')
    m.add_constr(z, t, '!=')
    m.add_constr(y, z, '<')
    m.arc_consistency('3')

import numpy as np
from src.Propagation import Propagation


class Variable:
    # domain: list, delta: np arrays
    def __init__(self, name, domain, delta, propagation):
        self.name = name
        self.domain = np.array(domain)
        self.domain_type = self.domain.dtype.name
        self.delta = delta
        self.propagation = propagation
        # list of couples <constraintType, variable>
        self.constraints = np.array([[]])

    def is_in_domain(self, a):
        if a in self.domain:
            return True
        return False

    def remove_value(self, a):
        # removing value a from domain
        self.domain = np.delete(self.domain, np.argwhere(self.domain == a))
        if self.is_in_domain(a):
            self.delta = np.append(self.delta, a)
            self.propagation.add_to_queue(self, a)

    def is_delta_empty(self):
        if self.delta.size == 0:
            return True
        return False

    def reset_delta(self):
        self.delta = np.array([])


if __name__ == '__main__':
    prop = Propagation()
    x = Variable(list(range(1,9)), [], prop)
    y = Variable(list(range(5,15)), [], prop)
    print('')
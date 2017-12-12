import numpy as np
from src.Propagation import Propagation


class Variable:
    # domain: list, delta: np arrays
    def __init__(self, name, domain, propagation):
        self.label = 0
        self.name = name
        self.domain = np.array(domain)
        self.delta = np.array([]).astype(int)
        self.propagation = propagation
        # list of couples <constraintType, variable>
        self.constraints = np.array([[]])

    def is_in_domain(self, a):
        if a in self.domain:
            return True
        return False

    def remove_value(self, a):
        if self.is_in_domain(a):
            self.delta = np.append(self.delta, a)
            self.propagation.add_to_queue(self)
        # removing value a from domain
        self.domain = np.delete(self.domain, np.argwhere(self.domain == a))

    def is_delta_empty(self):
        if len(self.delta) == 0:
            return True
        return False

    def reset_delta(self):
        self.delta = np.array([])

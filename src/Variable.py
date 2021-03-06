import numpy as np


class Variable:
    # domain: list, delta: np arrays
    def __init__(self, name, domain, propagation):
        self.label = False
        self.name = name
        self.domain = np.array(domain)
        self.delta = np.array([]).astype(int)
        self.propagation = propagation

    def is_in_domain(self, a):
        if self.domain.shape[0] == 0:
            return False
        return self.domain[0] <= a <= self.domain[self.domain.shape[0] - 1]

    def remove_value(self, a):
        if self.is_in_domain(a):
            self.delta = np.append(self.delta, a)
            self.propagation.add_to_queue(self)
        # removing value a from domain
        self.domain = np.delete(self.domain, np.argwhere(self.domain == a))

    def is_delta_empty(self):
        return len(self.delta) == 0

    def reset_delta(self):
        self.delta = np.array([])

import numpy as np


class Variable:
    # domain, delta: np arrays
    def __init__(self, domain, delta, propagation):
        self.domain = domain;
        self.delta = delta;
        self.propagation = propagation;

    def is_in_domain(self, a):
        if a in self.domain:
            return True
        return False

    def remove_value(self, a):
        # removing value a from domain
        self.domain = np.delete(self.domain, np.argwhere(self.domain == a))
        if self.is_in_domain(a):
            self.delta = np.append(self.delta, a)
            self.propagation.add_to_queue(self)

    def is_delta_empty(self):
        if self.delta.size == 0:
            return True
        return False

    def reset_delta(self):
        self.delta = np.array([])
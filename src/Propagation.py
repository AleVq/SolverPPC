import numpy as np
from src.AC3 import consistent
import sys


class Propagation:
    def __init__(self):
        self.queue = Queue()  # vars with a not-null Delta
        self.constr_graph = {}  # dictionary: <x_i, tuple_constraints>

    def update_constraints_graph(self, constraint):
        for var in [constraint.x, constraint.y]:
            name = var.name
            if name in self.constr_graph:
                self.constr_graph[name].append(constraint)
            else:
                self.constr_graph[name] = [constraint]

    def add_to_queue(self, x):
        if not self.queue.is_in(x):
            self.queue.enqueue(x)

    def pick_in_queue(self):
        return self.queue.dequeue()

    # return True if there are feasible solutions,
    # return False otherwise
    def run(self, vars):
        self.queue.enqueue(vars)
        while not self.queue.is_empty():
            x = self.pick_in_queue()
            for c in self.constr_graph[x.name]:
                if x == c.x:
                    c.filter_from(c.x)  # returns true if a value has been deleted
                    c.filter_from(c.y)
                else:
                    c.filter_from(c.y)
                    c.filter_from(c.x)
                if x.domain.shape[0] == 0:
                    return False  # one domain is empty, we stop here
            x.reset_delta()
        return True


class Queue:
    # vars: np array
    def __init__(self, variables = None):
        if variables is None:
            self.__queue = np.array([])
        else:
            self.__queue = variables

    def enqueue(self, x):
        self.__queue = np.append(self.__queue, x)

    def dequeue(self):
        var = self.__queue[0]
        self.__queue = np.delete(self.__queue, 0)
        return var

    def is_in(self, x):
        return x in self.__queue

    def is_empty(self):
        return self.__queue.size == 0

    def size(self):
        return self.__queue.shape[0]

    def print_queue(self):
        for v in self.__queue:
            sys.stdout.write(str(v.name) + ' ')
        print()

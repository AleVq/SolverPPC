import numpy as np
from src.AC3 import consistent


class Propagation:
    def __init__(self):
        self.queue = Queue()  # vars with a not-null Delta
        self.constr_graph = []  # array of couples: <x_i, tuple_constraints>

    def update_constraints_graph(self, constraint):
        for var in [constraint.x, constraint.y]:
            firsts = [item[0] for item in self.constr_graph]  # take all vars which
            # already are in the graph
            if var in firsts:
                index = firsts.index(var)
                self.constr_graph[index][1] = self.constr_graph[index][1] + (constraint,)
            else:
                self.constr_graph.append([var, (constraint,)])

    def add_to_queue(self, x):
        if not self.queue.is_in(x):
            self.queue.enqueue(x)

    def pick_in_queue(self):
        return self.queue.dequeue()

    '''def run(self, constraints):
        while not self.queue.is_empty():
            x = self.pick_in_queue()
            for c in [item for item in constraints if item.x == x]:
                ret = c.filter_from(x)
                if not ret:  # the domain is empty, we stop here
                    break
            x.reset_delta()'''
    def run(self, variables, constraints, prop):
        vars = self.backtrack([], variables, constraints)
        for x in vars:
            print('var: ' + str(x.name) + ' final value: ' + str(x.domain[0]))

    # lab: list, unlab, cons: np array
    # lab = vars with fixed value
    def backtrack(self, lab, unlab, cons):  # unlab = queue of Regin's propagation, lab = fixed-valued vars
        if unlab.shape[0] == 0:
            return lab
        x = unlab[0]
        # iterate over all values of x
        for v in x.domain:
            if self.lab_cons(v, x, lab, cons):
                x.delta.append(np.setdiff1d(x.domain, v))
                x.domain = np.array([v])
                new_lab = lab.copy()
                new_lab.append(x)
                z = unlab[0]
                result = self.backtrack(new_lab, np.delete(unlab, 0), cons)
                if len(result) != 0:
                    return result
        return []  # all values are inconsistent, must go back

    # return true if the value of x is consistent with the value
    # of the other variables with a single fixed value
    # v = value of x
    def lab_cons(self, v,  x, lab, cons):
        for c in cons:
            if c.x.name == x.name and c.y in lab and not consistent(v, c.y.domain[0], c.type):
                return False
            elif c.y.name == x.name and c.x in lab and not consistent(c.x.domain[0], v, c.type):
                return False
        return True


class Queue:
    def __init__(self):
        self.__queue = np.array([])

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

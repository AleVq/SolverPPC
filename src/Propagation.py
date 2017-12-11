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

    # return False if there are no feasible solutions,
    # return True otherwise
    def run(self, var):
        self.add_to_queue(var)
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

    # backtrack divers
    def run_selected_var(self, x, variables, constraints):
        c = np.delete(variables, np.argwhere(variables == x))
        queue = Queue(np.append([x], c))
        vars = self.backtrack_queue(np.array([]), queue, constraints)
        for x in vars:
            print('var: ' + str(x.name) + ' final value: ' + str(x.domain[0]))
        return vars

    def backtrack_queue(self, fixed_vars, queue, cons):  # unlab = queue of Regin's propagation, lab = fixed-valued vars
        print('vars')
        for var in fixed_vars:
            print(var.name)
        if queue.is_empty():
            return fixed_vars
        x = queue.dequeue()
        # iterate over all values of x
        for v in x.domain:
            #if x.name == 'x3':
                #print(x.domain)
                #print(x.delta)
            if self.lab_cons(v, x, fixed_vars, cons):
                x.delta.append(np.setdiff1d(x.domain, v))
                x.domain = np.array([v])
                result = self.backtrack_queue(np.append(fixed_vars, x), queue, cons)
                if result != []:
                    return result

        return []  # all values are inconsistent, must go back

    def run_backtrack(self, variables, constraints):
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
    def lab_cons(self, v,  x, fixed_vars, cons):
        for c in cons:
            if c.x.name == x.name and c.y in fixed_vars and not consistent(v, c.y.domain[0], c.type):
                return False
            elif c.y.name == x.name and c.x in fixed_vars and not consistent(c.x.domain[0], v, c.type):
                return False
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

    def to_string(self):
        for v in self.__queue:
            sys.stdout.write(str(v.name) + ' ')
        print()

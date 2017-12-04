import numpy as np


class Propagation:
    def __init__(self):
        self.queue = Queue()
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

    def run(self):
        while not self.queue.is_empty():
            x = self.pick_in_queue()
            for c in x.constraints:
                ret = c.filter_from(x)
                if not ret:
                    break
            x.reset_delta()


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
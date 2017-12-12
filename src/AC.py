from src.Constraint import Constraint
import sys
import numpy as np


def print_domains(c):
    print(str(c.x.name) + ' domain ' + str(c.x.domain))
    print(str(c.y.name) + ' domain ' + str(c.y.domain))


def consistent(x, y, expr):
    return eval(expr)


class AC3(Constraint):

    # var: Variable, revise method of AC3
    def filter_from(self, var):
        if var == self.x:
            x = self.x
            y = self.y
        else:
            x = self.y
            y = self.x
        deleted = False
        for v in x.domain:
            consistent_value = False
            for w in y.domain:
                if var == self.x:
                    if consistent(v, w, self.type):
                        consistent_value = True
                        break
                else:
                    if consistent(w, v, self.type):
                        consistent_value = True
                        break
            if not consistent_value:
                x.remove_value(v)
                deleted = True
        return deleted


class AC4(Constraint):
    def filter_from(self, x):
        for a in x.delta:
            key = str(x.name) + ', ' + str(a)
            if key in self.values_pairs.keys():
                for couple in self.values_pairs[key]:
                    if [x, a] in self.values_pairs[str(couple[0].name) + ', ' + str(couple[1])]:
                        self.values_pairs[str(couple[0].name) + ', ' + str(couple[1])].remove([x, a])
                    if len(self.values_pairs[str(couple[0].name) + ', ' + str(couple[1])]) == 0:
                        couple[0].remove_value(couple[1])

    def __init__(self, x, y, type, table=None):
        super(AC4, self).__init__(x, y, type, table)
        self.values_pairs = self.initialize()

    def initialize(self):
        counter = {}  # dict of couples: {'x, v': int}
        pairs = {}
        for x in [self.x, self.y]:
            for v in x.domain:
                pairs[str(x.name)+', '+str(v)] = []
                total = 0
                if x == self.x:
                    y = self.y
                    inverse = False
                else:
                    y = self.x
                    inverse = True
                for w in y.domain:
                    if inverse and consistent(w, v, self.type):
                        total += 1
                        if not [y, w] in pairs[str(x.name) + ', ' + str(v)]:
                            pairs[str(x.name) + ', ' + str(v)].append([y, w])
                    if consistent(v, w, self.type) and not inverse:
                        total += 1
                        if not [y, w] in pairs[str(x.name) + ', ' + str(v)]:
                            pairs[str(x.name) + ', ' + str(v)].append([y, w])
                counter[str(x.name)+', '+str(v)] = total
                if counter[str(x.name)+', '+str(v)] == 0:
                    x.remove_value(v)
        return pairs


class AC6(Constraint):

    def __init__(self, x, y, type, table=None):
        super(AC6, self).__init__(x, y, type, table)
        self.values_pairs = self.initialize()

    def initialize(self):
        pairs = {}  # dict of couples: {'x, v': int}
        for x in [self.x, self.y]:
            for v in x.domain:
                pairs[str(x.name)+', '+str(v)] = []
                if x == self.x:
                    y = self.y
                    inverse = False
                else:
                    y = self.x
                    inverse = True
                supported = False
                for w in y.domain:
                    if inverse and consistent(w, v, self.type):
                        pairs[str(x.name) + ', ' + str(v)].append([y, w])
                        supported = True
                        break
                    if consistent(v, w, self.type) and not inverse:
                        pairs[str(x.name) + ', ' + str(v)].append([y, w])
                        supported = True
                        break
                if not supported:
                    x.remove_value(v)
        return pairs

    def filter_from(self, x):
        for a in x.delta:
            key = str(x.name) + ', ' + str(a)
            if key in self.values_pairs.keys():
                for couple in self.values_pairs[key]:
                    new_support = self.exists_support(x, a, couple[0], couple[1])  # new_support: couple [x,c]
                    if new_support is None:
                        couple[0].remove_value(couple[1])
                    else:
                        key_ns = str(new_support[0].name) + ', ' + str(new_support[1])
                        if not couple in self.values_pairs[key_ns]:
                            self.values_pairs[key_ns].append(couple)

    def exists_support(self, x, a, y, b):
        for v in x.domain:
            # we know that y = c.x, x = c.y
            if v != a and consistent(b, v, self.type):
                return [x, v]
        return None

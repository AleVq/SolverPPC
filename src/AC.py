from src.Constraint import Constraint
import numpy as np


# x: in its domain we look for a new support
# y: its value b needs a new support
# used by AC-6 and AC-2001
def exists_support(c, x, a, y, b):
    next_val = np.where(x.domain > a)
    if len(next_val[0]) > 0:
        domain = x.domain[next_val[0][0]:]
        for v in domain:
            # we know that y = c.x, x = c.y
            if v != a and consistent(b, v, c.type):
                return [x, v]
    return None


# evaluating the constraint's expression
def consistent(x, y, expr):
    return eval(expr)


class AC3(Constraint):

    # var: Variable, revise method of AC3
    def filter_from(self, var):
        if var == self.y:
            x = self.x
            y = self.y
        else:
            x = self.y
            y = self.x
        deleted = False
        for v in x.domain:
            consistent_value = False
            for w in y.domain:
                if x == self.x:
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

    def __init__(self, x, y, type):
        super(AC4, self).__init__(x, y, type)
        self.values_pairs = self.initialize()

    def initialize(self):
        self.values_pairs = {}
        counter = {}  # dict of couples: {'x, v': int}
        pairs = {}
        for x in [self.x, self.y]:
            for v in x.domain:
                pairs[str(x.name) + ', ' + str(v)] = []
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
                counter[str(x.name) + ', ' + str(v)] = total
                if counter[str(x.name) + ', ' + str(v)] == 0:
                    x.remove_value(v)
        return pairs

    def filter_from(self, x):
        for a in x.delta:
            key = str(x.name) + ', ' + str(a)
            if key in self.values_pairs.keys():
                for couple in self.values_pairs[key]:
                    if [x, a] in self.values_pairs[str(couple[0].name) + ', ' + str(couple[1])]:
                        self.values_pairs[str(couple[0].name) + ', ' + str(couple[1])].remove([x, a])
                    if len(self.values_pairs[str(couple[0].name) + ', ' + str(couple[1])]) == 0:
                        couple[0].remove_value(couple[1])


class AC6(Constraint):

    def __init__(self, x, y, type):
        super(AC6, self).__init__(x, y, type)
        self.values_pairs = self.initialize()

    def initialize(self):
        self.values_pairs = {}
        pairs = {}  # dict of couples: {'x, v': int}
        for x in [self.x, self.y]:
            for v in x.domain:
                pairs[str(x.name) + ', ' + str(v)] = []
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
                    new_support = exists_support(self, x, a, couple[0], couple[1])  # new_support: couple [x,c]
                    if new_support is None:
                        couple[0].remove_value(couple[1])
                    else:
                        key_ns = str(new_support[0].name) + ', ' + str(new_support[1])
                        if key_ns == 'x0, 8':
                            print()
                        if not couple in self.values_pairs[key_ns]:
                            self.values_pairs[key_ns].append(couple)


class AC2001(Constraint):

    def __init__(self, x, y, type):
        super(AC2001, self).__init__(x, y, type)
        self.last = []  # last: dict of type {x, a, y, b}, where <y,b> is the last support of <x,a>
        self.initialize()

    def initialize(self):
        self.last = []
        for v in self.x.domain:
            found = False
            for w in self.y.domain:
                if consistent(v, w, self.type):
                    self.last.append([self.x, v, self.y, w])
                    found = True
                    break
            if not found:
                self.x.remove_value(v)
        for w in self.y.domain:
            found = False
            for v in self.x.domain:
                if consistent(v, w, self.type):
                    self.last.append([self.y, w, self.x, v])
                    found = True
                    break
            if not found:
                self.y.remove_value(w)

    def filter_from(self, x):
        for a in x.delta:
            for i in range(len(self.last)):
                if self.last[i][2] == x and self.last[i][3] == a:
                    new_support = exists_support(self, x, a, self.last[i][0], self.last[i][1])
                    if new_support is None:
                        self.last[i][0].remove_value(self.last[i][1])
                    else:
                        self.last[i][2] == new_support[0]
                        self.last[i][3] == new_support[1]

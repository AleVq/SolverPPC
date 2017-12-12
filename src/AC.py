from src.Constraint import Constraint


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

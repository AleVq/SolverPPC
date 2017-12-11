from src.Constraint import Constraint


def consistent(x, y, type):
    if type == '!=':
        return x != y
    elif type == '<':
        return x < y
    elif type == '>':
        return x > y


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

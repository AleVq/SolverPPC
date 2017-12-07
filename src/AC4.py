from src.Propagation import Queue
from src.AC3 import consistent

class AC4:

    def __init__(self):
        self.q = Queue()
        self.s = []
        self.counter = []

    def initialize(self, constraints):
        for arc in constraints:
            for v in arc.x.domain:
                total = 0
                for w in arc.y.domain:
                    if consistent(v, w, arc.type):
                        total += 1
                        consistent_arc = [arc.y, w, arc.x, v]
                        if not consistent_arc in self.s:
                            self.s.append(consistent_arc)
                if total == 0:
                    arc.x.remove_value(v)
                    self.q.enqueue()

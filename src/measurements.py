import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.Model import Model
from src.Model import char_range
import numpy as np
import pandas as pd


if __name__ == '__main__':
    upper_bound = 20
    measure = np.zeros((4, upper_bound-1)).tolist()
    for n in range(2, upper_bound+1):
        acs = [3, 4, 6, 2001]
        for x in acs:
            m = Model(x)
            for i in range(n):
                m.add_var(list(range(n)))
            for i in range((n-1)):
                for j in range((i+1), n):
                    a = j-i
                    m.add_constr(m.variables[i], m.variables[j], "x != y and x != (y-" +str(a) + ')' + " and x != (y+"+str(a) + ')')
            measure[acs.index(x)][n-2] = m.find_solution()
    measure = pd.DataFrame(measure).transpose()
    measure.columns = ['AC3', 'AC4', 'AC6', 'AC2001']
    measure.index += 2
    ax = measure.plot()
    ax.set_xlabel('number of queens')
    ax.set_ylabel('time to find solution (in seconds)')
    fig = ax.get_figure()
    fig.savefig('../results.eps', format='eps')
    fig = ax.get_figure()
    print(measure)

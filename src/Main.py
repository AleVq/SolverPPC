from src.Model import Model
from src.Model import char_range

if __name__ == '__main__':
    for x in [3, 4, 6, 2001]:
        m = Model(x)
        n = 16
        for i in range(n):
            m.add_var(list(range(n)))
        for i in range((n-1)):
            for j in range((i+1), n):
                a = j-i
                m.add_constr(m.variables[i], m.variables[j], "x != y and x != (y-" +str(a) + ')' + " and x != (y+"+str(a) + ')')
        m.find_solution()

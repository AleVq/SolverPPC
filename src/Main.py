from src.Model import Model

if __name__ == '__main__':
    for x in [3, 4, 6, 2001]:
        print('AC' + str(x) + ':')
        m = Model(x)
        # vars and constraints for n-queens problem
        n = 8
        for i in range(n):
            m.add_var(list(range(n)))
        for i in range((n-1)):
            for j in range((i+1), n):
                a = j-i
                m.add_constr(m.variables[i], m.variables[j], "x != y and x != (y-" +str(a) + ')' + " and x != (y+"+str(a) + ')')
        m.print_filtered_domains()
        m.find_solution()

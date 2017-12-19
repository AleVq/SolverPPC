# SolverPPC
University project consisting in creating a solver for the course of Constraint Programming.

This solver uses the backtrack algorithm in conjuction with AC (arc consistency algorithm) 
in order to find a solution to a given CSP problem. We can choose among AC3, AC4, AC6, AC2001.
In order to use this library it's sufficient to import the class Model, create an object of type Model,
defining variables and constraints. At last, we can call the method print_filtered_domains() to get the 
consistent domains or, if we want a solution to the problem, we can call the method find_solution().
Here's the example present in the file /src/Main.py:
```python
if __name__ == '__main__':
    # params of the constructor: 3 for AC3, 4 for AC4..
    m = Model(2001)
    # vars and constraints for n-queens problem
    n = 8
    for i in range(n):
        # to define a variable we only define its domain here, 
        # variables' names are managed by the API itself 
        # by naming the first inserted var x_0, the second x_1 and so on
        m.add_var(list(range(n)))
    # To add a constraint, we must give first var, second var and the type of constraint,
    # which is a string in which:
    # x must be used as a reference to the first constraint's variable,
    # y must be used as a reference to the second constraint's variable,
    # accepted operators are: >, =>, <, =<, !=, ==,
    # we are free to use expression like "x^2 > y+2*3/4 and x != y", 
    # i.e. Python math and logical operators are allowed (** for power)
    for i in range((n-1)):
        for j in range((i+1), n):
            a = j-i
            m.add_constr(m.variables[i], m.variables[j], "x != y and x != (y-" +str(a) + ')' + " and x != (y+"+str(a) + ')')
    m.print_filtered_domains()
    m.find_solution()
```

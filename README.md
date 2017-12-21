# SolverPPC
University project consisting in creating a solver for the course of Constraint Programming.

This solver uses the backtrack algorithm in conjuction with AC (arc consistency algorithm) 
in order to find a solution to a given CSP problem. We can choose among AC3, AC4, AC6, AC2001.

## How to use this library
In order to use this library it's sufficient to
* import the class Model,
* create an object of type Model by specifying which AC-algorithm we want to use, for example m = Model(3) if we want to use AC3,
* defining variables (at least 2),
* defining constraints (at least 1),
* we can call the method print_filtered_domains() to get the consistent domains obtained by using the AC algorithm,
* we can call the method find_solution(), if we want to get a solution of the problem, if it exists.

### Defining variables
To define a variable we need only define its domain here.
Domains are defined by an ordered vector (of any data type which supports comparison operators, such as int, float, chars, strings).
With integer-based domains the function range(n) can be used, with char-based domains the function char_range(c1, c2) has been implemented as well, which can returns ['a','b','c','d'] if given char_range('a','d'). Remember however that range(m, n) will output numbers from m to n-1.

Variables' names are managed by the API itself, by naming the first inserted variable x_0, the second x_1 and so on.

### Defining constraints
 To add a constraint, we need to define
 * the first variable, 
 * the second variable,
 * the type of constraint, i.e. a string in which:
    - x must be used as a reference to the first constraint's variable,
    - y must be used as a reference to the second constraint's variable,
    - accepted operators are: >, =>, <, =<, !=, ==.

By defing the type of constraint, we are free to use expression like "x^2 > (y+2*3/4) and x != y", i.e. Python math and logical operators are allowed (\*\* for power). For more details, please refer to Python's *eval* function.

Here's the example of 8-queens present in the file /src/Main.py:
```python
if __name__ == '__main__':
    # params of the constructor: 3 for AC3, 4 for AC4..
    m = Model(2001)
    # vars and constraints for n-queens problem
    n = 8
    # here all domains are [0,1..n-1]
    for i in range(n):
        m.add_var(list(range(n)))
    # thanks to the support of logical operators, we can compress different constraints
    # involving the same two variables in one single constraint
    for i in range((n-1)):
        for j in range((i+1), n):
            a = j-i
            m.add_constr(m.variables[i], m.variables[j], "x != y 
                                                       and x != (y-" +str(a) + ')' + 
                                                      " and x != (y+"+str(a) + ')')
    m.print_filtered_domains()
    m.find_solution()
```
## About complexity 
We can see with the example of the n-queens that backtrack using the AC3 algorithm is the fastest, since it doesn't have to reinitialize the structures used by the others AC at each backtrack step. Among the other AC algorithms, AC4 is the slowest by far, followed by AC6. AC2001 is the fastest AC with uses an additional structure.

Here is an example on how the different ACs behave on the nqueens problem for 2<=n<=16:

![Image of Performance](https://github.com/AleVq/SolverPPC/blob/master/results.png)

## How the library is structured
### Class Model
It's the hub of the library. The model contains all variables, constraints, the algorithm to find the consistent domains and the algorithm of backtrack.
### Class Variable
It contains the variable-related data and the methods of domain and delta update needed during the filtering.
### Class Constraint
It contains the basic constraint-related data. 
### Class Propagation 
It contains the methods needed to progagate the domain-related changes to all variables and constraints.
### Class AC
It contains all AC algorithms, which ereditate from the Constraint class. Each AC class contains the algorithm *filter_from(x)* which do the filtering of the constraint by basing itself on which variable had its domain changed.

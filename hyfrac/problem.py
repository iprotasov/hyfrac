class Problem:
    
    
    def __init__(self, parameters, variables):

        self.parameters = parameters
        self.variables = variables

        self.A = None
        self.B = None


    def F(self, x):

        return x*x

    def solve(self):

        x0 = self.variables.vector
        F = self.F
        x = fsolve(F, x0)

        new_variables = Variables.from_vector(x)

        return new_variables

class Model:


    def __init__(self, parameters=None, variables=None):
        self.parameters = parameters
        self.variables = variables


    def compute_next(self):
        
        # compute next model

        problem = Problem(parameters, variables)

        new_variables = problem.solve()
        
        new_model = Model(parameters, new_variables)

        return new_model


    def plot(self):

        # plot solution

        return fig


    def save(self, filename):

        # save model to file



import numpy as np
import solution
import parameters

class Model:


    def __init__(self, parameters=None):
        self.parameters = parameters
        self.solution = solution.Solution(self.parameters)


#    def compute_next(self):
#
#        # compute next model
#
#        problem = Problem(self.parameters, self.solution)
#
#        new_solution = problem.solve()
#
#        new_model = Model(parameters, new_solution)
#
#        return new_model
#
#
#    def plot(self):
#
#        # plot solution
#        fig = None
#
#        return fig
#
#
#    def save(self, filename):
#
#        # save model to file
#

if __name__ == '__main__':

    nu = 0.2
    dt = 1 # s
    dx = 1 # m
    E = 15/(1-0.2**2) # GPa
    mu = 12*0.02 # Pa*s
    K = 4*(2/np.pi)**(1/2)*1 # MPa*m^(1/2)
    Q = 0.0004*1e3 # [m^3/s]*10^-3
    h = 50 # m
    t = 10 # s
    Cp = 2*3*1e-6*1e3
    N = 5 # number of elements on each wing not including the center element
    # total number of elements is 2*N+1

    t_stop = 1000 # s

    parameters = parameters.Parameters(nu=nu,
                            E=E,
                            K=K,
                            Cp=Cp,
                            mu=mu,
                            Q=Q,
                            h=h,
                            N=N,
                            dt=dt,
                            t=t)
    model = Model(parameters)

def test():

    nu = 0.2
    dt = 1 # s
    dx = 1 # m
    E = 15/(1-0.2**2) # GPa
    mu = 12*0.02 # Pa*s
    K = 4*(2/np.pi)**(1/2)*1 # MPa*m^(1/2)
    Q = 0.0004*1e3 # [m^3/s]*10^-3
    h = 50 # m
    t = 10 # s
    Cp = 2*3*1e-6*1e3
    N = 5 # number of elements on each wing not including the center element
    # total number of elements is 2*N+1

    t_stop = 1000 # s

    params = parameters.Parameters(nu=nu,
                            E=E,
                            K=K,
                            Cp=Cp,
                            mu=mu,
                            Q=Q,
                            h=h,
                            N=N,
                            dt=dt,
                            t=t)
    model = Model(params)

    return model.solution

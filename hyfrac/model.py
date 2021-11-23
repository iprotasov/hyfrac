import numpy as np
import solution
import parameters
import problem
import copy

class Model:


    def __init__(self, parameters, solution_=None):

        self.parameters = parameters

        if solution_:
            self.solution = solution_
        else:
            self.solution = solution.Solution(self.parameters)


    def asdict(self):
        return {'parameters': self.parameters.asdict(),
                'solution': self.solution.asdict()}


    @classmethod
    def fromdict(cls, in_dict):
        parameters_ = parameters.Parameters.fromdict(in_dict['parameters'])
        solution_ = solution.Solution.fromdict(in_dict['solution'])
        return cls(parameters_, solution_)


    def compute_next(self):

        # compute next model

        self.problem = problem.Problem(self.parameters, self.solution)

        try:
            new_solution = self.problem.solve()
        except Exception as e: raise

        new_parameters = copy.deepcopy(self.parameters)
        new_parameters.t += self.parameters.dt
        new_model = Model(new_parameters, new_solution)

        return new_model


if __name__ == '__main__':

    nu = 0.2
    dt = 1 # s
    dx = 1 # m
    E = 15/(1-0.2**2) # GPa
    mu = 12*0.02 # Pa*s
    mu = 12*1e-10 # Pa*s
    K = 4*(2/np.pi)**(1/2)*1 # MPa*m^(1/2)
    Q = 0.0004*1e3 # [m^3/s]*10^-3
    h = 50 # m
    t = 100 # s
    Cp = 2*3*1e-6*1e3
    N = 2 # number of elements on each wing not including the center element
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
    mu = 12*1e-6 # Pa*s
    K = 4*(2/np.pi)**(1/2)*1 # MPa*m^(1/2)
    Q = 0.0004*1e3 # [m^3/s]*10^-3
    h = 50 # m
    t = 100 # s
    Cp = 2*3*1e-6*1e3
    N = 4 # number of elements on each wing not including the center element
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

    new_model = model.compute_next()

    return model, new_model


def compute_initial_solution(nu,
                            E,
                            K,
                            Cp,
                            mu,
                            Q,
                            h,
                            N,
                            dt,
                            t):

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

    return model



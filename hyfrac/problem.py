import copy
import operators
import numpy as np
import scipy.optimize

class Problem:


    def __init__(self, parameters, solution):

        self.parameters = parameters
        self.solution = solution


    def F(self, w):

        dt = self.parameters.dt
        x = self.solution.x_vector
        dx = self.solution.dl_vector
        w0 = self.solution.w_vector

        A = operators.flow(x, dx, w, self.parameters)
        C = operators.elasticity(x, dx, self.parameters)
        Matr = np.eye(len(x)) + dt*A.dot(C)
        b = copy.deepcopy(w0).transpose()
        b[x==0] += dt*self.parameters.Q/dx[x==0]/self.parameters.h

        #RHS=w(i-1,:)' + dt*q'/h - leakoff_term;

        return (Matr.dot(w) - b) / np.linalg.norm(b)

    def solve(self):

        x0 = self.solution.w_vector
        x, infodict, ier, mesg = scipy.optimize.fsolve(self.F, x0, full_output=True)
        if ier != 1:
            raise Exception(f'fsolve not converged, msg = {mesg}')

        new_solution = copy.deepcopy(self.solution)
        new_solution.w_vector = x

        return new_solution



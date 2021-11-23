import copy
import operators
import numpy as np
import scipy.optimize

class Problem:


    def __init__(self, parameters, solution):

        self.parameters = parameters
        self.solution = solution

        self.convergence = []

        self.v0_solution = None
        self.Matr = None
        self.b = None


    def set_tip_element(self, solution_copy):

        x = solution_copy.x_vector
        dx = solution_copy.dl_vector
        w = solution_copy.w_vector
        h = solution_copy.h_vector

        alpha = np.sqrt(9*np.pi/128) * self.parameters.E / self.parameters.K
        v = [0, 0]
        v[0] = ( alpha * w[0] * dx[0] )**(2/3)
        v[-1] = ( alpha * w[-1] * dx[-1] )**(2/3)

        if v[0] > dx[0] and v[0] < 2*dx[1]:
            x[0] -= (v[0]-dx[0]) / 2
            w[0] *= dx[0]/v[0]
            dx[0] = v[0]
        if v[-1] > dx[-1] and v[-1] < 2*dx[-2]:
            x[-1] += (v[-1]-dx[-1]) / 2
            w[-1] *= dx[-1]/v[-1]
            dx[-1] = v[-1]

        dx_add = [0, 0]
        x_add = [0, 0]
        w_add = [0, 0]
        if v[0] >= 2*dx[1]:
            print('hey')
            vol = dx[0]*w[0]
            vol_tip = vol * ( (v[0] - dx[1]) / v[0] )**(1.5)
            x[0] -= (dx[1]-dx[0]) / 2
            x_add[0] = x[0] - v[0]/2
            dx[0] = dx[1]
            dx_add[0] = v[0] - dx[0]
            w_add[0] = vol_tip / dx_add[0]
            w[0] = (vol - vol_tip) / dx[0]
            dx = np.concatenate([[dx_add[0]], dx])
            x = np.concatenate([[x_add[0]], x])
            w = np.concatenate([[w_add[0]], w])
            h = np.concatenate([[h[0]], h])

        if v[-1] >= 2*dx[-2]:
            vol = dx[-1]*w[-1]
            vol_tip = vol * ( (v[-1] - dx[-2]) / v[-1] )**(1.5)
            x[-1] += (dx[-2]-dx[-1]) / 2
            x_add[-1] = x[-1] + v[-1]/2
            dx[-1] = dx[-2]
            dx_add[-1] = v[-1] - dx[-1]
            w_add[-1] = vol_tip / dx_add[-1]
            w[-1] = (vol - vol_tip) / dx[-1]
            dx = np.concatenate([dx, [dx_add[-1]]])
            x = np.concatenate([x, [x_add[-1]]])
            w = np.concatenate([w, [w_add[0]]])
            h = np.concatenate([h, [h[-1]]])

        solution_copy.dl_vector = dx
        solution_copy.x_vector = x
        solution_copy.w_vector = w
        solution_copy.h_vector = h

    def F(self, w):

        #solution_copy = copy.deepcopy(self.solution)
        #self.set_tip_element(w, solution_copy)

        dt = self.parameters.dt
        x = self.v0_solution.x_vector
        dx = self.v0_solution.dl_vector
        w0 = self.v0_solution.w_vector

        if True:
       # if not self.Matr:
            A = operators.flow(x, dx, w, self.parameters)
            C = operators.elasticity(x, dx, self.parameters)
            self.Matr = np.eye(len(x)) + dt*A.dot(C)

        if True:
        #if not self.b:
            self.b = copy.deepcopy(w0).transpose()
            self.b[x==0] += dt*self.parameters.Q/dx[x==0]/self.parameters.h


        #RHS=w(i-1,:)' + dt*q'/h - leakoff_term;


        #w_as = @(s) (1+delta1)*w_next(1)*dx(1)/s;

        self.convergence.append(np.linalg.norm((self.Matr.dot(w) - self.b) ) / np.linalg.norm(self.b))

        #return (self.Matr.dot(w) - self.b) / np.linalg.norm(self.b)
        return (self.Matr.dot(w) - self.b) / np.linalg.norm(self.b) - (np.minimum(w,0)**2)*1e6


    def solve(self):

        self.v0_solution = copy.deepcopy(self.solution)
        self.set_tip_element(self.v0_solution)
        v0 = self.v0_solution.w_vector

        v, infodict, ier, mesg = scipy.optimize.fsolve(self.F, v0, full_output=True, xtol=1e-5)
        if ier != 1:
            raise Exception(f'fsolve not converged, msg = {mesg}')

        new_solution = copy.deepcopy(self.v0_solution)
        new_solution.w_vector = v

        #self.set_tip_element(v, new_solution)

        return new_solution



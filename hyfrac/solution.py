import numpy as np
import operators

class Solution:


    def __init__(self, parameters=None):

        fracture_volume = parameters.Q * parameters.t
        fracture_length = parameters.h
        fracture_width = fracture_volume / (parameters.h * fracture_length)
        N = parameters.N

        num_total = 2*N + 1
        num_inner = num_total - 2

        dl = fracture_length / num_total

        self.fracture_volume = fracture_volume
        self.w_vector = np.ones(num_total) * fracture_width
        self.h_vector = np.ones(num_total) * parameters.h
        self.dl_vector = np.ones(num_total) * dl
        self.phi_vector = None
        self.x_vector = np.linspace(-N*dl, N*dl, 2*N+1)
        self.y_vector = None

        self.c_matrix = operators.elasticity(self.x_vector, self.dl_vector, parameters)
        unit_w = np.linalg.solve(self.c_matrix, np.ones(num_total))
        self.w_vector = unit_w * fracture_volume / ((unit_w*self.h_vector*self.dl_vector).sum())
        self.p_vector = self.c_matrix.dot(self.w_vector)


import numpy as np
import operators

class Solution:


    def __init__(self, parameters=None, in_dict=None):

        if in_dict:
            self.w_vector = np.array(in_dict['w_vector'])
            self.h_vector = np.array(in_dict['h_vector'])
            self.dl_vector = np.array(in_dict['dl_vector'])
            self.x_vector = np.array(in_dict['x_vector'])
            self.y_vector = np.array(in_dict['y_vector'])
            self.p_vector = np.array(in_dict['p_vector'])
        else:

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

    def asdict(self):
        return {'w_vector': self.w_vector,
                'h_vector': self.h_vector,
                'dl_vector': self.dl_vector,
                'x_vector': self.x_vector,
                'y_vector': self.y_vector,
                'p_vector': self.p_vector}

    @classmethod
    def fromdict(cls, in_dict):
        return cls(in_dict=in_dict)


    def get_x_plot(self):
        return np.concatenate([[self.x_vector[0]-self.dl_vector[0]/2], self.x_vector, [self.x_vector[-1]+self.dl_vector[-1]/2]])

    def get_w_plot(self):
            return np.concatenate([[0], self.w_vector, [0]])

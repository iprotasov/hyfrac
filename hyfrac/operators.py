import numpy as np

def elasticity(x, dx, parameters):
    E = parameters.E
    sv, xv = np.meshgrid(x, x)
    dxv, _ = np.meshgrid(dx, x)
    c_matrix = -E/(4*np.pi) * ( dxv / ((xv-sv)**2 - (dxv/2)**2) )
    return c_matrix

def flow():
    A = None
    return A

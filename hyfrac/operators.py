import numpy as np

def elasticity(x, dx, parameters):
    E = parameters.E
    sv, xv = np.meshgrid(x, x)
    dxv, _ = np.meshgrid(dx, x)
    c_matrix = -E/(4*np.pi) * ( dxv / ((xv-sv)**2 - (dxv/2)**2) )
    return c_matrix

def flow(x, dx, w, parameters):
#    alpha = -12/(np.pi**2)/parameters.mu # PKN
    alpha = -1/parameters.mu # KGD
    A = np.zeros((len(x),len(x)))

    for i in range(0,len(x)-1):
        A[i][i+1] += alpha / dx[i] * ( ( w[i] + w[i+1] ) / 2 )**3 / ( (dx[i]+dx[i + 1])/2 )
        A[i][i] -= A[i][i+1]

    for i in range(1,len(x)):
        A[i][i-1] += alpha / dx[i] * ( ( w[i-1] + w[i] ) / 2 )**3 / ( (dx[i-1]+dx[i])/2 )
        A[i][i] -= A[i][i-1]

    return A

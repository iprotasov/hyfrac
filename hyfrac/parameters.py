from dataclasses import dataclass
import dataclasses

@dataclass
class Parameters:
    
    nu: float
    E: float
    K: float
    Cp: float
    mu: float
    Q: float
    h: float
    N: float
    dt: float
    t: float

    def asdict(self):
        return dataclasses.asdict(self)

    @classmethod
    def fromdict(cls, in_dict):
        nu = in_dict['nu']
        E = in_dict['E']
        K = in_dict['K']
        Cp = in_dict['Cp']
        mu = in_dict['mu']
        Q = in_dict['Q']
        h = in_dict['h']
        N = in_dict['N']
        dt = in_dict['dt']
        t = in_dict['t']
        return cls(nu=nu,
                   E=E,
                   K=K,
                   Cp=Cp,
                   mu=mu,
                   Q=Q,
                   h=h,
                   N=N,
                   dt=dt,
                   t=t)

class Variables:


    def __init__(self, w=None, dx=None, h=None):

        self.w = w
        self.dx = dx
        self.h = h


    @classmethod
    def from_vector(cls, vector):

        # create variables from vector

        return cls(w, dx, h)

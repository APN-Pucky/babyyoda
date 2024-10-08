class loc:
    "When used in the start or stop of a Histogram's slice, x is taken to be the position in data coordinates."

    def __init__(self, x, offset=0):
        self.value = x
        self.offset = offset

    # add and subtract method
    def __add__(self, other):
        return loc(self.value, self.offset + other)

    def __sub__(self, other):
        return loc(self.value, self.offset - other)


class rebin:
    "When used in the step of a Histogram's slice, rebin(n) combines bins, scaling their widths by a factor of n. If the number of bins is not divisible by n, the remainder is added to the overflow bin."

    def __init__(self, factor):
        self.factor = factor


class underflow:
    pass


class overflow:
    pass

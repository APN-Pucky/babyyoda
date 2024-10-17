import gzip
import inspect
import sys


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


class project:
    pass


def open_write_file(file_path, gz=False):
    if file_path.endswith((".gz", ".gzip")) or gz:
        return gzip.open(file_path, "wt")
    return open(file_path, "w")


def uses_yoda(obj):
    if hasattr(obj, "target"):
        return uses_yoda(obj.target)
    return is_yoda(obj)


def is_yoda(obj):
    return is_from_package(obj, "yoda.")


def is_from_package(obj, package_name):
    # Get the class of the object
    obj_class = obj.__class__

    # Get the method resolution order (MRO) of the class, which includes parent classes
    mro = inspect.getmro(obj_class)

    # Check each class in the MRO for its module
    for cls in mro:
        module = inspect.getmodule(cls)
        if module and module.__name__.startswith(package_name):
            return True
    return False


def has_own_method(cls, method_name):
    # Check if the class has the method defined
    if not hasattr(cls, method_name):
        return False

    # Get the method from the class and the parent class
    cls_method = getattr(cls, method_name)
    parent_method = getattr(cls.__bases__[0], method_name, None)

    # Compare the underlying function (__func__) if both exist
    return cls_method.__func__ is not parent_method.__func__


def rebinBy_to_rebinTo(edges: list[float], factor: int, begin=1, end=sys.maxsize):
    # Just compute the new edges and call rebinXTo
    start = begin - 1
    stop = end
    if start is None:
        start = 0
    stop = (len(edges) - 1) if stop >= sys.maxsize else stop - 1
    new_edges = []
    # new_bins = []
    # new_bins += [self.underflow()]
    for i in range(start):
        # new_bins.append(self.bins()[i].clone())
        new_edges.append(edges[i])
        new_edges.append(edges[i + 1])
    last = None
    for i in range(start, stop, factor):
        if i + factor <= (len(edges) - 1):
            xmin = edges[i]
            xmax = edges[i + 1]
            # nb = GROGU_HISTO1D_V3.Bin()
            for j in range(factor):
                last = i + j
                # nb += self.bins()[i + j]
                xmin = min(xmin, edges[i + j])
                xmax = max(xmax, edges[i + j + 1])
            # new_bins.append(nb)
            # add both edges
            new_edges.append(xmin)
            new_edges.append(xmax)
    for j in range(last + 1, (len(edges) - 1)):
        # new_bins.append(self.bins()[j].clone())
        new_edges.append(edges[j])
        new_edges.append(edges[j + 1])
    # no duplicates
    return list(set(new_edges))

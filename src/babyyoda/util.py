import gzip
import inspect


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

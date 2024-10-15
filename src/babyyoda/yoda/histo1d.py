import yoda
from packaging import version

import babyyoda
from babyyoda.util import has_own_method


class Histo1D(babyyoda.UHIHisto1D):
    def __init__(self, *args, **kwargs):
        """
        target is either a yoda or grogu HISTO1D_V2
        """

        target = args[0] if len(args) == 1 else yoda.Histo1D(*args, **kwargs)
        # unwrap target
        while isinstance(target, Histo1D):
            target = target.target

        super().__setattr__("target", target)

    ########################################################
    # Relay all attribute access to the target object
    ########################################################

    def __getattr__(self, name):
        # if we overwrite it here, use that
        if has_own_method(Histo1D, name):
            return getattr(self, name)
        # if the target has the attribute, use that
        if hasattr(self.target, name):
            return getattr(self.target, name)
        # lastly use the inherited attribute
        if hasattr(super(), name):
            return getattr(super(), name)
        err = f"'{type(self).__name__}' object and target have no attribute '{name}'"
        raise AttributeError(err)

    def __setattr__(self, name, value):
        if has_own_method(Histo1D, name):
            setattr(self, name, value)
        elif hasattr(self.target, name):
            setattr(self.target, name, value)
        elif hasattr(super(), name):
            setattr(super(), name, value)
        else:
            err = f"Cannot set attribute '{name}'; it does not exist in target or Forwarder."
            raise AttributeError(err)

    def __call__(self, *args, **kwargs):
        # If the target is callable, forward the call, otherwise raise an error
        if callable(self.target):
            return self.target(*args, **kwargs)
        err = f"'{type(self.target).__name__}' object is not callable"
        raise TypeError(err)

    def bins(self, includeOverflows=False, *args, **kwargs):
        import yoda

        if version.parse(yoda.__version__) >= version.parse("2.0.0"):
            return self.target.bins(*args, includeOverflows=includeOverflows, **kwargs)
        # YODA1 does not offer inlcudeOverflows
        if includeOverflows:
            return [
                self.target.underflow(),
                *self.target.bins(),
                self.target.overflow(),
            ]
        return self.target.bins(*args, **kwargs)

    def rebinXTo(self, *args, **kwargs):
        import yoda

        if version.parse(yoda.__version__) >= version.parse("2.0.0"):
            return self.target.rebinXTo(*args, **kwargs)
        return self.target.rebinTo(*args, **kwargs)

    def rebinXBy(self, *args, **kwargs):
        import yoda

        if version.parse(yoda.__version__) >= version.parse("2.0.0"):
            return self.target.rebinXBy(*args, **kwargs)
        return self.target.rebinBy(*args, **kwargs)

    def __getitem__(self, slices):
        return super().__getitem__(slices)

    def clone(self):
        return Histo1D(self.target.clone())

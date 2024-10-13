import yoda

import babyyoda


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
        # First, check if the Forwarder object itself has the attribute
        if name in self.__dict__ or hasattr(type(self), name):
            return object.__getattribute__(self, name)
        # If not, forward attribute access to the target
        if hasattr(self.target, name):
            return getattr(self.target, name)
        err = f"'{type(self).__name__}' object and target have no attribute '{name}'"
        raise AttributeError(err)

    def __setattr__(self, name, value):
        # First, check if the attribute belongs to the Forwarder itself
        if name in self.__dict__ or hasattr(type(self), name):
            object.__setattr__(self, name, value)
        # If not, forward attribute setting to the target
        elif hasattr(self.target, name):
            setattr(self.target, name, value)
        else:
            err = f"Cannot set attribute '{name}'; it does not exist in target or Forwarder."
            raise AttributeError(err)

    def __call__(self, *args, **kwargs):
        # If the target is callable, forward the call, otherwise raise an error
        if callable(self.target):
            return self.target(*args, **kwargs)
        err = f"'{type(self.target).__name__}' object is not callable"
        raise TypeError(err)

    def __getitem__(self, slices):
        return super().__getitem__(slices)

    def clone(self):
        return Histo1D(self.target.clone())

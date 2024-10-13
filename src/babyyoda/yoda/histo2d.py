import babyyoda


class Histo2D(babyyoda.Histo2D):
    def __init__(self, *args, **kwargs):
        """
        target is either a yoda or grogu HISTO2D_V2
        """
        if len(args) == 1:
            target = args[0]
            # Store the target object where calls and attributes will be forwarded
        else:
            import yoda

            target = yoda.Histo2D(*args, **kwargs)

        # unwrap target
        while isinstance(target, Histo2D):
            target = target.target

        # Store the target object where calls and attributes will be forwarded
        super().__setattr__("target", target)

    ########################################################
    # Relay all attribute access to the target object
    ########################################################

    def __getattr__(self, name):
        # yoda-1 has overflow but yoda-2 does not so we patch it in here
        if name in self.__dict__ or hasattr(type(self), name):
            return object.__getattribute__(self, name)
        elif hasattr(self.target, name):
            return getattr(self.target, name)
        raise AttributeError(
            f"'{type(self).__name__}' object and target have no attribute '{name}'"
        )

    def __setattr__(self, name, value):
        # First, check if the attribute belongs to the Forwarder itself
        if name in self.__dict__ or hasattr(type(self), name):
            object.__setattr__(self, name, value)
        # If not, forward attribute setting to the target
        elif hasattr(self.target, name):
            setattr(self.target, name, value)
        else:
            raise AttributeError(
                f"Cannot set attribute '{name}'; it does not exist in target or Forwarder."
            )

    def __call__(self, *args, **kwargs):
        # If the target is callable, forward the call, otherwise raise an error
        if callable(self.target):
            return self.target(*args, **kwargs)
        raise TypeError(f"'{type(self.target).__name__}' object is not callable")

    def __getitem__(self, slices):
        return super().__getitem__(slices)

    def clone(self):
        return Histo2D(self.target.clone())

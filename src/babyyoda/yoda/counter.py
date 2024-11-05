from typing import Any, Optional

import yoda

import babyyoda
from babyyoda.util import has_own_method


class Counter(babyyoda.UHICounter):
    def __init__(self, *args: list[Any], **kwargs: dict[Any, Any]) -> None:
        """
        target is either a yoda or grogu Counter
        """
        if len(args) == 1 and isinstance(args[0], yoda.Counter):
            target = args[0]
        elif len(args) == 1 and isinstance(args[0], Counter):
            target = args[0].target
        else:
            target = yoda.Counter(*args, **kwargs)

        super().__setattr__("target", target)

    ########################################################
    # Relay all attribute access to the target object
    ########################################################

    def __getattr__(self, name: str):
        # if we overwrite it here, use that
        if has_own_method(Counter, name):
            return getattr(self, name)
        # if the target has the attribute, use that
        if hasattr(self.target, name):
            return getattr(self.target, name)
        # lastly use the inherited attribute
        if hasattr(super(), name):
            return getattr(super(), name)
        err = f"'{type(self).__name__}' object and target have no attribute '{name}'"
        raise AttributeError(err)

    # def __setattr__(self, name, value):
    #    if has_own_method(Counter, name):
    #        setattr(self, name, value)
    #    elif hasattr(self.target, name):
    #        setattr(self.target, name, value)
    #    elif hasattr(super(), name):
    #        setattr(super(), name, value)
    #    else:
    #        err = f"Cannot set attribute '{name}'; it does not exist in target or Forwarder."
    #        raise AttributeError(err)

    # def __call__(self, *args, **kwargs):
    #    # If the target is callable, forward the call, otherwise raise an error
    #    if callable(self.target):
    #        return self.target(*args, **kwargs)
    #    err = f"'{type(self.target).__name__}' object is not callable"
    #    raise TypeError(err)

    def bins(self, *args, **kwargs) -> Any:
        return self.target.bins(*args, **kwargs)

    def clone(self) -> "Counter":
        return Counter(self.target.clone())

    # Fix https://gitlab.com/hepcedar/yoda/-/issues/101
    def annotationsDict(self) -> dict[str, Optional[str]]:
        d = {}
        for k in self.target.annotations():
            d[k] = self.target.annotation(k)
        return d

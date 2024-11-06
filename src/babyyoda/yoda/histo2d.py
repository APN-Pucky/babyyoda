from typing import Any, Optional, cast

import yoda
from packaging import version

import babyyoda
from babyyoda.util import has_own_method
from babyyoda.yoda.histo1d import Histo1D


class Histo2D(babyyoda.UHIHisto2D):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        target is either a yoda or grogu HISTO2D_V2
        """
        if isinstance(args[0], yoda.Histo2D):
            target = args[0]
        elif isinstance(args[0], Histo2D):
            target = args[0].target
        else:
            target = yoda.Histo2D(*args, **kwargs)

        # Store the target object where calls and attributes will be forwarded
        super().__setattr__("target", target)

    ##########################
    # Basic needed functions for UHI directly relayed to target
    ##########################

    def clone(self) -> "Histo2D":
        return Histo2D(self.target.clone())

    def path(self) -> str:
        return str(self.target.path())

    def bins(self, includeOverflows: bool = False, *args: Any, **kwargs: Any) -> Any:
        import yoda

        if version.parse(yoda.__version__) >= version.parse("2.0.0"):
            return self.target.bins(*args, includeOverflows=includeOverflows, **kwargs)
        if not includeOverflows:
            # YODA1 bins are not sorted than YODA2
            return sorted(
                self.target.bins(*args, **kwargs), key=lambda b: (b.yMin(), b.xMin())
            )
        err = "YODA1 backend can not include overflows"
        raise NotImplementedError(err)

    def xEdges(self) -> list[float]:
        return cast(list[float], self.target.xEdges())

    def yEdges(self) -> list[float]:
        return cast(list[float], self.target.yEdges())

    def rebinXTo(self, bins: list[float]) -> None:
        self.target.rebinXTo(bins)

    def rebinYTo(self, bins: list[float]) -> None:
        self.target.rebinYTo(bins)

    def get_projector(self) -> Any:
        return Histo1D

    # Fix https://gitlab.com/hepcedar/yoda/-/issues/101
    def annotationsDict(self) -> dict[str, Optional[str]]:
        d = {}
        for k in self.target.annotations():
            d[k] = self.target.annotation(k)
        return d

    ########################################################
    # Relay all attribute access to the target object
    ########################################################

    def __getattr__(self, name: Any) -> Any:
        # if we overwrite it here, use that
        if has_own_method(Histo2D, name):
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
    #    if has_own_method(Histo2D, name):
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

    def __getitem__(self, slices: Any) -> Any:
        return super().__getitem__(slices)

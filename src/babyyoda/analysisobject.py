class UHIAnalysisObject:
    ########
    # Basic needed functions for UHI+YODA
    ########
    def path(self) -> str:
        err = "UHIAnalysisObject.path() must be implemented by subclass"
        raise NotImplementedError(err)

    def setAnnotation(self, key: str, value: str) -> None:
        err = "UHIAnalysisObject.setAnnotation() must be implemented by subclass"
        raise NotImplementedError(err)

    def key(self) -> str:
        return self.path()

    def setAnnotationsDict(self, d: dict[str, str]) -> None:
        for k, v in d.items():
            self.setAnnotation(k, v)

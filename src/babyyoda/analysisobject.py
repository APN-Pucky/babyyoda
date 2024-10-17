class UHIAnalysisObject:
    def key(self):
        return self.path()

    def setAnnotationsDict(self, d: dict):
        for k, v in d.items():
            self.setAnnotation(k, v)

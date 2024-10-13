from dataclasses import dataclass


@dataclass
class GROGU_ANALYSIS_OBJECT:
    d_key: str = ""
    # d_name: str  = ""
    d_type: str = ""
    d_title: str = ""
    d_path: str = "/"
    # d_scaled_by: float = 1.0 #TODO maybe we want to track ScaledBy in the future

    ############################################
    # YODA compatibilty code
    ############################################

    def key(self):
        return self.d_key

    def path(self):
        return self.d_path

    def name(self):
        return self.path().split("/")[-1]

    def title(self):
        return self.d_title

    def type(self):
        return self.d_type

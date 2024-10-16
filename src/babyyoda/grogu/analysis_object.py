import re
from dataclasses import dataclass, field


@dataclass
class GROGU_ANALYSIS_OBJECT:
    d_annotations: dict = field(default_factory=dict)
    # TODO add anotations
    d_key: str = ""

    def __post_init__(self):
        if "Path" not in self.d_annotations:
            self.d_annotations["Path"] = "/"
        if "Title" not in self.d_annotations:
            self.d_annotations["Title"] = ""

    ############################################
    # YODA compatibilty code
    ############################################

    def key(self):
        return self.d_key

    def name(self):
        return self.path().split("/")[-1]

    def path(self):
        p = self.annotation("Path")
        return p if p else "/"

    def title(self):
        return self.annotation("Title")

    def type(self):
        return self.annotation("Type")

    def annotations(self):
        return self.d_annotations.keys()

    def annotation(self, k: str, default=None) -> str:
        return self.d_annotations.get(k, default)

    def setAnnotation(self, key: str, value: str):
        self.d_annotations[key] = value

    def clearAnnotations(self):
        self.d_annotations = {}

    def hasAnnotation(self, key: str) -> bool:
        return key in self.d_annotations

    def annotationsDict(self):
        return self.d_annotations

    @classmethod
    def from_string(cls, file_content: str) -> "GROGU_ANALYSIS_OBJECT":
        lines = file_content.strip().splitlines()
        # Extract metadata (path, title)
        annotations = {"Path": "/"}
        pattern = re.compile(r"(\S+): (.+)")
        for line in lines:
            pattern_match = pattern.match(line)
            if pattern_match:
                annotations[pattern_match.group(1).strip()] = pattern_match.group(
                    2
                ).strip()
            elif line.startswith("---"):
                break

        return cls(
            d_annotations=annotations,
            d_key=annotations.get("Path", ""),
        )

    def to_string(self):
        ret = ""
        for k, v in self.d_annotations.items():
            val = v
            if val is None:
                val = "~"  # Weird YODA NULL strings cf. YAML-cpp
            ret += f"{k}: {val}\n"
        return ret

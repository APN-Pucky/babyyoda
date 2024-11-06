import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GROGU_ANALYSIS_OBJECT:
    d_annotations: dict[str, Optional[str]] = field(default_factory=dict)
    d_key: str = ""

    def __post_init__(self) -> None:
        if "Path" not in self.d_annotations:
            self.d_annotations["Path"] = "/"
        if "Title" not in self.d_annotations:
            self.d_annotations["Title"] = ""

    ############################################
    # YODA compatibility code
    ############################################

    def key(self) -> str:
        return self.d_key

    def name(self) -> str:
        return self.path().split("/")[-1]

    def path(self) -> str:
        p = self.annotation("Path")
        return p if p else "/"

    def title(self) -> Optional[str]:
        return self.annotation("Title")

    def type(self) -> Optional[str]:
        return self.annotation("Type")

    def annotations(self) -> list[str]:
        return list(self.d_annotations.keys())

    def annotation(self, k: str, default: Optional[str] = None) -> Optional[str]:
        return self.d_annotations.get(k, default)

    def setAnnotation(self, key: str, value: str) -> None:
        self.d_annotations[key] = value

    def clearAnnotations(self) -> None:
        self.d_annotations = {}

    def hasAnnotation(self, key: str) -> bool:
        return key in self.d_annotations

    def annotationsDict(self) -> dict[str, Optional[str]]:
        return self.d_annotations

    @classmethod
    def from_string(cls, file_content: str) -> "GROGU_ANALYSIS_OBJECT":
        lines = file_content.strip().splitlines()
        # Extract metadata (path, title)
        annotations: dict[str, Optional[str]] = {"Path": "/"}
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
            d_key=annotations.get("Path", "") or "",
        )

    def to_string(self) -> str:
        ret = ""
        for k, v in self.d_annotations.items():
            val = v
            if val is None:
                val = "~"  # Weird YODA NULL strings cf. YAML-cpp
            ret += f"{k}: {val}\n"
        return ret

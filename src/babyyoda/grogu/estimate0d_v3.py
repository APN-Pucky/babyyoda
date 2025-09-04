import re
import warnings
from dataclasses import dataclass, field

import numpy as np

from babyyoda.analysisobject import UHIAnalysisObject
from babyyoda.grogu.analysis_object import GROGU_ANALYSIS_OBJECT


@dataclass
class GROGU_ESTIMATE0D_V3(GROGU_ANALYSIS_OBJECT, UHIAnalysisObject):
    """A GROGU Estimate0D V3 object representing uncertainty estimates for a scalar value."""

    d_value: float = 0.0
    d_error_labels: list[str] = field(default_factory=list)
    d_errors_dn: list[float] = field(default_factory=list)
    d_errors_up: list[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()
        if "Type" not in self.d_annotations:
            self.d_annotations["Type"] = "Estimate0D"

    # Value access methods
    def value(self) -> float:
        """Get the central value."""
        return self.d_value

    def val(self) -> float:
        """Get the central value (alias)."""
        return self.d_value

    def quadSum(self) -> tuple[float, float]:
        """Calculate total downward and upward errors by summing in quadrature."""
        total_dn = (
            np.sqrt(np.sum([err**2 for err in self.d_errors_dn if not np.isnan(err)]))
            if self.d_errors_dn
            else float("nan")
        )
        total_up = (
            np.sqrt(np.sum([err**2 for err in self.d_errors_up if not np.isnan(err)]))
            if self.d_errors_up
            else float("nan")
        )
        return (-total_dn, total_up)

    def totalErr(self) -> tuple[float, float]:
        """Get total error (alias for quadSum)."""
        return self.quadSum()

    def totalErrAvg(self) -> float:
        """Get average of absolute total errors."""
        return 0.5 * np.sum(np.abs(self.totalErr()))

    def errors_dn(self) -> list[float]:
        """Get downward errors for all error sources."""
        return self.d_errors_dn

    def errors_up(self) -> list[float]:
        """Get upward errors for all error sources."""
        return self.d_errors_up

    def error_labels(self) -> list[str]:
        """Get error source labels."""
        return self.d_error_labels

    def has_nan(self) -> bool:
        """Check if this estimate contains NaN values."""
        return np.isnan(self.d_value) or any(
            np.isnan(err) for err in self.d_errors_dn + self.d_errors_up
        )

    def error_dn(self, label_idx: int = 0) -> float:
        """Get downward error for a specific error source."""
        return (
            self.d_errors_dn[label_idx]
            if label_idx < len(self.d_errors_dn)
            else float("nan")
        )

    def error_up(self, label_idx: int = 0) -> float:
        """Get upward error for a specific error source."""
        return (
            self.d_errors_up[label_idx]
            if label_idx < len(self.d_errors_up)
            else float("nan")
        )

    def num_error_sources(self) -> int:
        """Get number of error sources."""
        return len(self.d_error_labels)

    @classmethod
    def from_string(cls, file_content: str) -> "GROGU_ESTIMATE0D_V3":
        """Parse Estimate0D V3 from string content."""
        lines = file_content.strip().splitlines()

        # Extract key from first line
        key = ""
        if find := re.search(r"BEGIN YODA_ESTIMATE0D_V3 (\S+)", lines[0]):
            key = find.group(1)

        # Parse annotations from base class
        annotations = GROGU_ANALYSIS_OBJECT.from_string(file_content).d_annotations

        # Initialize parsing variables
        value = 0.0
        error_labels = []
        errors_dn = []
        errors_up = []
        data_section_started = False
        value_parsed = False

        for tline in lines:
            line = tline.strip()

            if line.startswith("BEGIN YODA_ESTIMATE0D_V3"):
                continue
            if line.startswith("END YODA_ESTIMATE0D_V3"):
                break
            if line.startswith("#") or not line:
                continue
            if line.startswith("---"):
                data_section_started = True
                continue

            if not data_section_started:
                continue

            # Parse error labels
            if line.startswith("ErrorLabels:"):
                content = re.findall(r"\[(.*?)\]", line)[0]
                # Parse the labels, removing quotes
                label_strings = [s.strip().strip('"') for s in content.split(",")]
                error_labels = [s for s in label_strings if s]
                continue

            # Skip the header line with column names
            if line.startswith(("# value", "#value")):
                continue

            # Parse data line (single value with errors)
            if not line.startswith("#") and not value_parsed:
                try:
                    parts = re.split(r"\s+", line.strip())

                    # Parse value
                    value_str = parts[0]
                    value = float("nan") if value_str == "nan" else float(value_str)

                    # Parse errors
                    # Skip value column, parse error pairs
                    for i in range(1, len(parts), 2):
                        if i + 1 < len(parts):
                            dn_str = parts[i]
                            up_str = parts[i + 1]

                            # Handle "---" which means no error
                            if dn_str == "---":
                                errors_dn.append(float("nan"))
                            else:
                                errors_dn.append(float(dn_str))

                            if up_str == "---":
                                errors_up.append(float("nan"))
                            else:
                                errors_up.append(float(up_str))

                    value_parsed = True
                except (ValueError, IndexError) as e:
                    # Skip malformed lines with a proper warning
                    warnings.warn(
                        f"Could not parse line '{line}' in Estimate0D V3 object with key '{key}': {e}. Skipping malformed line.",
                        UserWarning,
                        stacklevel=2,
                    )
                    continue

        return cls(
            d_annotations=annotations,
            d_key=key,
            d_value=value,
            d_error_labels=error_labels,
            d_errors_dn=errors_dn,
            d_errors_up=errors_up,
        )

    def to_string(self) -> str:
        """Convert Estimate0D V3 to string representation."""
        header = (
            f"BEGIN YODA_ESTIMATE0D_V3 {self.d_key}\n"
            f"{GROGU_ANALYSIS_OBJECT.to_string(self)}"
            "---\n"
        )

        # Format error labels
        label_str = ", ".join(f'"{label}"' for label in self.d_error_labels)
        error_labels = f"ErrorLabels: [{label_str}]\n"

        # Format column headers
        column_headers = ["# value"]
        for i, _ in enumerate(self.d_error_labels, start=1):
            column_headers.extend([f"errDn({i})", f"errUp({i})"])
        header_line = "\t".join(column_headers) + "\t\n"

        # Format value data
        value_str = "nan" if np.isnan(self.d_value) else f"{self.d_value:.6e}"
        parts = [value_str]

        for dn, up in zip(self.d_errors_dn, self.d_errors_up):
            if np.isnan(dn):
                parts.append("---")
            else:
                parts.append(f"{dn:.6e}")

            if np.isnan(up):
                parts.append("---")
            else:
                parts.append(f"{up:.6e}")

        value_line = "\t".join(parts) + "\t"

        footer = "END YODA_ESTIMATE0D_V3"

        return f"{header}{error_labels}{header_line}{value_line}\n{footer}"

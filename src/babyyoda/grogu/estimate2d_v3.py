import re
import warnings
from dataclasses import dataclass, field
from typing import Any

import numpy as np

from babyyoda.analysisobject import UHIAnalysisObject
from babyyoda.grogu.analysis_object import GROGU_ANALYSIS_OBJECT


@dataclass
class GROGU_ESTIMATE2D_V3(GROGU_ANALYSIS_OBJECT, UHIAnalysisObject):
    """A GROGU Estimate2D V3 object representing uncertainty estimates for 2D histogram bins."""

    @dataclass
    class Bin:
        """A bin for Estimate2D containing value and error estimates."""

        d_value: float = 0.0
        d_error_labels: list[str] = field(default_factory=list)
        d_errors_dn: list[float] = field(default_factory=list)
        d_errors_up: list[float] = field(default_factory=list)

        def value(self) -> float:
            return self.d_value

        def val(self) -> float:
            return self.d_value

        def quadSum(self) -> tuple[float, float]:
            """Calculate total downward and upward errors by summing in quadrature."""
            total_dn = (
                np.sqrt(
                    np.sum([err**2 for err in self.d_errors_dn if not np.isnan(err)])
                )
                if self.d_errors_dn
                else float("nan")
            )
            total_up = (
                np.sqrt(
                    np.sum([err**2 for err in self.d_errors_up if not np.isnan(err)])
                )
                if self.d_errors_up
                else float("nan")
            )
            return (-total_dn, total_up)

        def totalErr(self) -> tuple[float, float]:
            return self.quadSum()

        def totalErrAvg(self) -> float:
            return 0.5 * np.sum(np.abs(self.totalErr()))

        def errors_dn(self) -> list[float]:
            return self.d_errors_dn

        def errors_up(self) -> list[float]:
            return self.d_errors_up

        def error_labels(self) -> list[str]:
            return self.d_error_labels

        def has_nan(self) -> bool:
            """Check if this bin contains NaN values."""
            return np.isnan(self.d_value) or any(
                np.isnan(err) for err in self.d_errors_dn + self.d_errors_up
            )

        @classmethod
        def from_string(
            cls, line: str, error_labels: list[str]
        ) -> "GROGU_ESTIMATE2D_V3.Bin":
            """Parse a bin from a string line."""
            parts = re.split(r"\s+", line.strip())

            # Parse value
            value_str = parts[0]
            value = float("nan") if value_str == "nan" else float(value_str)

            # Parse errors
            errors_dn = []
            errors_up = []

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

            return cls(
                d_value=value,
                d_error_labels=error_labels.copy(),
                d_errors_dn=errors_dn,
                d_errors_up=errors_up,
            )

        def to_string(self) -> str:
            """Convert bin to string representation."""
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

            return "\t".join(parts) + "\t"

    d_bins: list[Bin] = field(default_factory=list)
    d_edges: list[list[float]] = field(default_factory=list)  # [x_edges, y_edges]
    d_error_labels: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()
        if "Type" not in self.d_annotations:
            self.d_annotations["Type"] = "Estimate2D"

    # UHI compatibility methods
    def bins(self, includeOverflows: bool = False) -> np.typing.NDArray[Any]:
        if includeOverflows:
            return np.array(self.d_bins)
        # TODO consider represent data always as numpy
        return (
            np.array(self.d_bins)
            .reshape((len(self.yEdges()) + 1, len(self.xEdges()) + 1))[1:-1, 1:-1]
            .flatten()
        )

    def xEdges(self) -> list[float]:
        """Get X bin edges."""
        return self.d_edges[0] if len(self.d_edges) > 0 else []

    def yEdges(self) -> list[float]:
        """Get Y bin edges."""
        return self.d_edges[1] if len(self.d_edges) > 1 else []

    def edges(self) -> list[list[float]]:
        """Get all edges."""
        return self.d_edges

    def values(self) -> list[float]:
        """Get bin values."""
        return [bin.value() for bin in self.d_bins]

    def error_labels(self) -> list[str]:
        """Get error source labels."""
        return self.d_error_labels

    def errors_dn(self, label_idx: int = 0) -> list[float]:
        """Get downward errors for a specific error source."""
        return [
            (
                bin.errors_dn()[label_idx]
                if label_idx < len(bin.errors_dn())
                else float("nan")
            )
            for bin in self.d_bins
        ]

    def errors_up(self, label_idx: int = 0) -> list[float]:
        """Get upward errors for a specific error source."""
        return [
            (
                bin.errors_up()[label_idx]
                if label_idx < len(bin.errors_up())
                else float("nan")
            )
            for bin in self.d_bins
        ]

    def num_bins(self) -> int:
        """Get number of bins."""
        return len(self.d_bins)

    def num_edges(self) -> int:
        """Get total number of edges."""
        return sum(len(edges) for edges in self.d_edges)

    def num_x_bins(self) -> int:
        """Get number of X bins."""
        return len(self.xEdges()) - 1 if self.xEdges() else 0

    def num_y_bins(self) -> int:
        """Get number of Y bins."""
        return len(self.yEdges()) - 1 if self.yEdges() else 0

    @classmethod
    def from_string(cls, file_content: str) -> "GROGU_ESTIMATE2D_V3":
        """Parse Estimate2D V3 from string content."""
        lines = file_content.strip().splitlines()

        # Extract key from first line
        key = ""
        if find := re.search(r"BEGIN YODA_ESTIMATE2D_V3 (\S+)", lines[0]):
            key = find.group(1)

        # Parse annotations from base class
        annotations = GROGU_ANALYSIS_OBJECT.from_string(file_content).d_annotations

        # Initialize parsing variables
        bins = []
        edges = []
        error_labels = []
        data_section_started = False

        for tline in lines:
            line = tline.strip()

            if line.startswith("BEGIN YODA_ESTIMATE2D_V3"):
                continue
            if line.startswith("END YODA_ESTIMATE2D_V3"):
                break
            if line.startswith("#") or not line:
                continue
            if line.startswith("---"):
                data_section_started = True
                continue

            if not data_section_started:
                continue

            # Parse edges for both axes
            if line.startswith(("Edges(A1):", "Edges(A2):")):
                content = re.findall(r"\[(.*?)\]", line)[0]
                # Split by comma and convert to floats
                edge_strings = [s.strip() for s in content.split(",")]
                edge_list = [float(s) for s in edge_strings if s]
                edges.append(edge_list)
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

            # Parse data lines (bins)
            if not line.startswith("#"):
                try:
                    bin_obj = cls.Bin.from_string(line, error_labels)
                    bins.append(bin_obj)
                except (ValueError, IndexError) as e:
                    # Skip malformed lines with a proper warning
                    warnings.warn(
                        f"Could not parse line '{line}': {e}. Skipping malformed line.",
                        UserWarning,
                        stacklevel=2,
                    )
                    continue

        return cls(
            d_annotations=annotations,
            d_key=key,
            d_bins=bins,
            d_edges=edges,
            d_error_labels=error_labels,
        )

    def to_string(self) -> str:
        """Convert Estimate2D V3 to string representation."""
        header = (
            f"BEGIN YODA_ESTIMATE2D_V3 {self.d_key}\n"
            f"{GROGU_ANALYSIS_OBJECT.to_string(self)}"
            "---\n"
        )

        # Format edges for both axes
        edges_str = ""
        for i, edge_list in enumerate(self.d_edges, start=1):
            edge_str = ", ".join(f"{edge:.6e}" for edge in edge_list)
            edges_str += f"Edges(A{i}): [{edge_str}]\n"

        # Format error labels
        label_str = ", ".join(f'"{label}"' for label in self.d_error_labels)
        error_labels = f"ErrorLabels: [{label_str}]\n"

        # Format column headers
        column_headers = ["# value"]
        for i, _ in enumerate(self.d_error_labels, start=1):
            column_headers.extend([f"errDn({i})", f"errUp({i})"])
        header_line = "\t".join(column_headers) + "\t\n"

        # Format bin data
        bin_data = "\n".join(bin.to_string() for bin in self.d_bins)

        footer = "END YODA_ESTIMATE2D_V3"

        return f"{header}{edges_str}{error_labels}{header_line}{bin_data}\n{footer}"

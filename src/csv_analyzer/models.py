from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ColumnStats:
    name: str
    dtype: str
    count: int
    missing: int
    missing_pct: float
    unique: int
    mean: Optional[float] = None
    median: Optional[float] = None
    std: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    top_values: list[str] = field(default_factory=list)
    outliers: list[float] = field(default_factory=list)
    outlier_count: int = 0

@dataclass
class AnalysisResult:
    filename: str
    row_count: int
    col_count: int
    columns: list[ColumnStats]

    @property
    def has_missing(self) -> bool:
        return any(col.missing > 0 for col in self.columns)
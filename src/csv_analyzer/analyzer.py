import statistics
from collections import Counter
from .models import ColumnStats, AnalysisResult


def _is_numeric(values: list[str]) -> bool:
    non_empty = [v for v in values if v.strip()]
    if not non_empty:
        return False
    try:
        [float(v) for v in non_empty]
        return True
    except ValueError:
        return False
    
def _detect_outliers(nums: list[float]) -> list[float]:
    if len(nums) < 4:
        return []
    
    sorted_nums = sorted(nums)
    n = len(sorted_nums)
    
    q1 = sorted_nums[n // 4]
    q3 = sorted_nums[(n * 3) // 4]
    iqr = q3 - q1
    
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    
    return [x for x in nums if x < lower or x > upper]


def _analyze_column(name: str, raw_values: list[str]) -> ColumnStats:
    count = len(raw_values)
    missing = sum(1 for v in raw_values if not v.strip())
    non_empty = [v for v in raw_values if v.strip()]
    unique = len(set(non_empty))

    stats = ColumnStats(
        name=name,
        dtype="numeric" if _is_numeric(raw_values) else "categorical",
        count=count,
        missing=missing,
        missing_pct=round(missing / count * 100, 2) if count else 0.0,
        unique=unique,
    )

    if stats.dtype == "numeric":
        nums = [float(v) for v in non_empty]
        stats.mean   = round(statistics.mean(nums), 4)
        stats.median = round(statistics.median(nums), 4)
        stats.std    = round(statistics.stdev(nums), 4) if len(nums) > 1 else 0.0
        stats.min    = min(nums)
        stats.max    = max(nums)
        stats.outliers = _detect_outliers(nums)
        stats.outlier_count = len(stats.outliers)
    else:
        top = Counter(non_empty).most_common(5)
        stats.top_values = [v for v, _ in top]

    return stats


def analyze(
    headers: list[str],
    rows: list[dict],
    filename: str = "unknown",
) -> AnalysisResult:
    columns = [
        _analyze_column(h, [row.get(h, "") for row in rows])
        for h in headers
    ]
    return AnalysisResult(
        filename=filename,
        row_count=len(rows),
        col_count=len(headers),
        columns=columns,
    )
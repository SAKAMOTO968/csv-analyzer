import json
from pathlib import Path
from csv_analyzer.models import AnalysisResult, ColumnStats
from csv_analyzer.reporter import to_dict, export_json

def make_result() -> AnalysisResult:
    return AnalysisResult(
            filename="test.csv",
            row_count=3,
            col_count=2,
            columns=[
                ColumnStats(
                    name="age", dtype="numeric", count=3, missing=1, missing_pct=33.33, unique=2,
                    mean=30.0, median=30.0, std=1.0, min=29.0, max=31.0,
                ),
                ColumnStats(
                    name="city", dtype="categorical", count=3, missing=0, missing_pct=0.0, unique=2,
                    top_values=["Bangkok", "Chiang Mai"],
                ),
            ],

    )
    
def test_to_dict_has_required_keys():
    d = to_dict(make_result())
    assert d["filename"] == "test.csv"
    assert d["row_count"] == 3
    assert len(d["columns"]) == 2
    
def test_to_dict_numeric_column():
    d = to_dict(make_result())
    age = d["columns"][0]
    assert age["name"] == "age"
    assert age["dtype"] == "numeric"
    assert age["mean"] == 30.0

def test_to_dict_categorical_column():
    d = to_dict(make_result())
    city = d["columns"][1]
    assert city["name"] == "city"
    assert city["dtype"] == "categorical"
    assert city["unique"] == 2
    assert city["top_values"] == ["Bangkok", "Chiang Mai"]

def test_export_json_creates_file(tmp_path: Path):
    result = make_result()
    output_file = tmp_path / "output.json"
    export_json(result, output_file)
    assert output_file.exists()
    data = json.loads(output_file.read_text())
    assert data["filename"] == "test.csv"
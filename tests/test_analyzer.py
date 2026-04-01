from csv_analyzer.analyzer import analyze, _is_numeric


def test_numeric_detection():
    assert _is_numeric(["1.5", "2.0", "3"]) is True
    assert _is_numeric(["hello", "world"]) is False
    assert _is_numeric(["", "", ""]) is False


def test_missing_percentage():
    headers = ["age"]
    rows = [{"age": "25"}, {"age": ""}, {"age": "30"}, {"age": ""}]
    result = analyze(headers, rows)
    col = result.columns[0]
    assert col.missing == 2
    assert col.missing_pct == 50.0


def test_mean_calculation():
    headers = ["score"]
    rows = [{"score": "90"}, {"score": "85"}]
    result = analyze(headers, rows)
    assert result.columns[0].mean == 87.5


def test_has_missing_property():
    headers = ["x"]
    rows = [{"x": "1"}, {"x": ""}]
    result = analyze(headers, rows)
    assert result.has_missing is True
    
def test_no_outliers_in_normal_data():
    headers = ["score"]
    rows = [{"score": str(v)} for v in [10, 11, 12, 13, 14, 15]]
    result = analyze(headers, rows)
    assert result.columns[0].outlier_count == 0
    
def test_detects_outlier():
    headers = ["score"]
    rows = [{"score": str(v)} for v in [10, 11, 12, 13, 14, 999]]
    result = analyze(headers, rows)
    assert 999.0 in result.columns[0].outliers
    assert result.columns[0].outlier_count == 1
    
def test_analyze_specific_columns():
    headers = ["name", "age", "salary"]
    rows = [
        {"name": "Alice", "age": "30", "salary": "70000"},
        {"name": "Bob", "age": "25", "salary": "50000"},
        {"name": "Charlie", "age": "", "salary": "60000"},
    ]
    selected = [h for h in headers if h in ["age", "salary"]]
    result = analyze(selected, rows)
    
    assert result.col_count == 2
    assert result.columns[0].name == "age"
    assert result.columns[1].name == "salary"
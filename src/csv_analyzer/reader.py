import csv
from pathlib import Path

class CSVReadError(Exception):
    pass

def read_csv(filepath: str | Path) -> tuple[list[str], list[dict]]:
    path = Path(filepath)
    
    if not path.exists():
        raise CSVReadError(f"File not found: {path}")
    if path.suffix.lower() != ".csv":
        raise CSVReadError(f"Expected .csv file, got: {path.suffix}")
    
    try:
        with path.open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise CSVReadError("CSV file is empty")
            headers = list(reader.fieldnames)
            rows = list(reader)
    except UnicodeDecodeError as e:
        raise CSVReadError(f"Cannot decode file: {e}") from e
    
    return headers, rows
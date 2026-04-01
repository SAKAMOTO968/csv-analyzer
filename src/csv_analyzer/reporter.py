import json
from dataclasses import asdict
from pathlib import Path
from .models import AnalysisResult

def to_dict(result: AnalysisResult) -> dict:
    d = asdict(result)
    clean_columns = [
        {k: v for k, v in col.items() if v is not None}
        for col in d["columns"]
    ]
    d["columns"] = clean_columns
    return d

def export_json(result: AnalysisResult, output_path: str | Path) -> None:
    """Write analysis result to a JSON file.
    
    Args:
        result: the analysis result to export
        output_path: where to write the JSON file
        
    Raises:
        OSError: if the file cannot be written
    """
    path = Path(output_path)
    data = to_dict(result)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Exported to {path}")
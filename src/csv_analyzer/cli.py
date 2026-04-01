import argparse
from pathlib import Path
from .reader import read_csv, CSVReadError
from .analyzer import analyze
from .reporter import export_json

def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a CSV file")
    parser.add_argument("filepath", help="Path to CSV file")
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="Export result to JSONN file (e.g. --output result.json)",
    )
    args = parser.parse_args()
    
    try:
        headers, rows = read_csv(args.filepath)
        result = analyze(headers, rows, filename=Path(args.filepath).name)
    except CSVReadError as e:
        print(f"Error: {e}")
        return

    print(f"\nFile: {result.filename}")
    print(f"Rows: {result.row_count}  |  Columns: {result.col_count}")
    print(f"Has missing values: {result.has_missing}\n")

    for col in result.columns:
        print(f"  [{col.dtype}] {col.name}")
        print(f"    missing: {col.missing} ({col.missing_pct}%)  unique: {col.unique}")
        if col.dtype == "numeric":
            print(f"    mean: {col.mean}  median: {col.median}  std: {col.std}")
            print(f"    min: {col.min}  max: {col.max}")
            if col.outlier_count > 0:                                          
                print(f"    outliers ({col.outlier_count}): {col.outliers}")   
        else:
            print(f"    top values: {', '.join(col.top_values)}")
        print()
        
    if args.output:
        try:
            export_json(result, args.output)
        except OSError as e:
            print(f"Export failed: {e}")


if __name__ == "__main__":
    main()
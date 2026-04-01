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
        help="Export result to JSON file (e.g. --output result.json)",
    )
    parser.add_argument(
    "--columns",
    metavar="COLS",
    help="Columns to analyze, comma-separated (e.g. --columns age,salary)",
    )
    args = parser.parse_args()
    
    try:
        headers, rows = read_csv(args.filepath)
        
        if args.columns:
            selected = [c.strip() for c in args.columns.split(",")]
            invalid = [c for c in selected if c not in headers]
            if invalid:
                print(f"Error: columns not found: {', '.join(invalid)}")
                print(f"Available: {', '.join(headers)}")
                return
            headers = selected
            
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
# CSV Analyzer

CLI tool for analyzing CSV files. Detects column types, calculates statistics, finds outliers, and exports results to JSON.

## Installation

\\ash
python -m venv .venv
.venv/Scripts/activate
pip install -e .[dev]
\
## Usage

\\ash
# Basic analysis
csv-analyzer data.csv

# Export to JSON
csv-analyzer data.csv --output result.json
\
## Example output

\File: sample.csv
Rows: 5  |  Columns: 4
Has missing values: True

  [numeric] age
    missing: 1 (20.0%)  unique: 4
    mean: 33.5  median: 32.0  std: 6.455
    min: 28.0  max: 42.0

  [categorical] department
    missing: 1 (20.0%)  unique: 2
    top values: Engineering, Marketing
\
## Running tests

\\ash
pytest tests/ -v
\
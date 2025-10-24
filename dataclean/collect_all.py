import csv
from typing import Iterable, List

def merge_csvs(filenames: Iterable[str], output_file: str, encoding: str = "utf-8") -> None:
    """
    Merge CSV files that share the same set of columns.
    - Keeps the header/column order from the first file.
    - Aligns later files by column name (order may differ).
    - Raises if any file has a different set of columns.

    Args:
        filenames: Iterable of CSV file paths (at least one).
        output_file: Path to the merged CSV.
        encoding: File encoding (default 'utf-8').
    """
    filenames = list(filenames)
    if not filenames:
        raise ValueError("No input files provided.")

    # Read the first file to establish canonical header order
    with open(filenames[0], newline="", encoding=encoding) as f0:
        r0 = csv.DictReader(f0)
        if not r0.fieldnames:
            raise ValueError(f"No header found in: {filenames[0]}")
        header: List[str] = list(r0.fieldnames)
        first_rows = list(r0)  # buffer rows from the first file

    # Open output and write header
    with open(output_file, "w", newline="", encoding=encoding) as fo:
        w = csv.DictWriter(fo, fieldnames=header)
        w.writeheader()

        # Emit buffered rows from the first file
        for row in first_rows:
            w.writerow({c: row.get(c, "") for c in header})

        # Process the remaining files
        for path in filenames[1:]:
            with open(path, newline="", encoding=encoding) as f:
                r = csv.DictReader(f)
                if not r.fieldnames:
                    raise ValueError(f"No header found in: {path}")

                cols = list(r.fieldnames)

                # Validate same column set (names must match, order can differ)
                if set(cols) != set(header):
                    raise ValueError(
                        f"Column mismatch in {path}\nExpected: {header}\nFound:    {cols}"
                    )

                # Emit rows aligned by the canonical header
                for row in r:
                    w.writerow({c: row.get(c, "") for c in header})

# --- Example (remove or adapt) ---
# merge_csvs(
#     ["data/a.csv", "data/b.csv", "data/c.csv"],
#     "merged.csv"
# )

merge_csvs(["country/Argentina.csv","country/Australia.csv","country/Canada.csv","country/Greece.csv","country/India.csv","country/United States.csv"],"merge_csv.csv")
import csv
from typing import Iterable, Optional, List, Tuple, Set

def subtract_csv(
    a_csv: str,
    b_csv: str,
    out_csv: str,
    *,
    keys: Optional[List[str]] = None,   # compare by these columns; if None, compare by ALL columns in A
    allow_reorder: bool = True,         # if True, B may have columns in a different order
    case_insensitive: bool = False,     # comparison option
    strip_ws: bool = True,              # trim whitespace before comparing
    encoding: str = "utf-8",
) -> int:
    """
    Write to out_csv all rows from A that are NOT present in B.
    Returns the number of rows written.

    - If keys is None: rows are identical if ALL columns in A match by name.
      (B must contain at least those columns; extra columns in B are ignored.)
    - If keys is provided: identical means those key columns match.
    - Column order differences are fine when allow_reorder=True.
    """

    def norm(v: object) -> str:
        s = "" if v is None else str(v)
        if strip_ws:
            s = s.strip()
        if case_insensitive:
            s = s.lower()
        return s

    # --- Read headers ---
    with open(a_csv, newline="", encoding=encoding) as fa:
        ra = csv.DictReader(fa)
        if not ra.fieldnames:
            raise ValueError(f"No header in {a_csv}")
        cols_a = list(ra.fieldnames)
        a_rows = list(ra)  # buffer A to keep order

    with open(b_csv, newline="", encoding=encoding) as fb:
        rb = csv.DictReader(fb)
        if not rb.fieldnames:
            raise ValueError(f"No header in {b_csv}")
        cols_b = list(rb.fieldnames)
        b_rows = list(rb)

    # --- Decide comparison columns ---
    if keys is None:
        # Compare by all columns from A. Ensure B has them.
        comp_cols = cols_a
        missing = [c for c in comp_cols if c not in cols_b]
        if missing:
            raise ValueError(f"{b_csv} is missing columns required for comparison: {missing}")
    else:
        comp_cols = list(keys)
        missing_a = [c for c in comp_cols if c not in cols_a]
        missing_b = [c for c in comp_cols if c not in cols_b]
        if missing_a:
            raise ValueError(f"{a_csv} missing key columns: {missing_a}")
        if missing_b:
            raise ValueError(f"{b_csv} missing key columns: {missing_b}")

    # If not allowing reorder and comparing all columns, require identical header order
    if keys is None and not allow_reorder and cols_a != cols_b:
        raise ValueError(
            "Column order differs between A and B. "
            "Set allow_reorder=True or align headers."
        )

    # --- Build set of comparison keys from B ---
    def key_from_row(row: dict) -> Tuple[str, ...]:
        return tuple(norm(row.get(c, "")) for c in comp_cols)

    seen_in_b: Set[Tuple[str, ...]] = set(key_from_row(r) for r in b_rows)

    # --- Write A minus B ---
    written = 0
    with open(out_csv, "w", newline="", encoding=encoding) as fo:
        w = csv.DictWriter(fo, fieldnames=cols_a)
        w.writeheader()
        for row in a_rows:
            if key_from_row(row) not in seen_in_b:
                w.writerow(row)
                written += 1

    return written

# -------------------------
# Examples:
# 1) Exact row subtraction (all columns must match):
subtract_csv("final_vaccine_age_group.csv", "fk_violations_rows.csv", "final_minus_age.csv")
#
# 2) Subtract by key columns only (e.g., isoCode+date+vaccine):
# subtract_csv("A.csv", "B.csv", "A_minus_B.csv", keys=["isoCode","date","vaccine"])
#
# 3) Case-insensitive, trim spaces when comparing:
# subtract_csv("A.csv", "B.csv"_

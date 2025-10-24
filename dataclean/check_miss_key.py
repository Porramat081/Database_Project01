import csv
from typing import Iterable, Tuple, Set, Optional

def check_fk_iso_date(
    fact_csv: str,                 # first CSV (child / FK holder)
    ref_csv: str,                  # second CSV (reference / parent)
    *,
    iso_col: str = "isoCode",
    date_col: str = "date",
    case_insensitive_iso: bool = True,
    strip_ws: bool = True,
    violations_out_csv: Optional[str] = None,   # write child rows with missing FK here (optional)
    missing_keys_out_csv: Optional[str] = None  # write just the missing keys here (optional)
) -> Tuple[int, int]:
    """
    Checks that every (isoCode, date) in `fact_csv` exists in `ref_csv`.
    Returns (violating_row_count, distinct_missing_key_count).

    If `violations_out_csv` is provided, writes full violating rows from `fact_csv`.
    If `missing_keys_out_csv` is provided, writes unique (isoCode, date) pairs that were missing.
    """
    def norm_iso(s: str) -> str:
        if s is None: return ""
        s = s.strip() if strip_ws else s
        return s.lower() if case_insensitive_iso else s

    def norm_date(s: str) -> str:
        if s is None: return ""
        return s.strip() if strip_ws else s

    # --- Build reference key set from parent ---
    ref_keys: Set[Tuple[str, str]] = set()
    with open(ref_csv, newline="", encoding="utf-8") as fr:
        rr = csv.DictReader(fr)
        for needed in (iso_col, date_col):
            if needed not in (rr.fieldnames or []):
                raise KeyError(f"{ref_csv} missing column '{needed}'")
        for row in rr:
            ref_keys.add((norm_iso(row.get(iso_col, "")),
                          norm_date(row.get(date_col, ""))))

    # --- Scan child and collect violations ---
    violations = []
    missing_keys: Set[Tuple[str, str]] = set()

    with open(fact_csv, newline="", encoding="utf-8") as ff:
        rf = csv.DictReader(ff)
        for needed in (iso_col, date_col):
            if needed not in (rf.fieldnames or []):
                raise KeyError(f"{fact_csv} missing column '{needed}'")

        for row in rf:
            key = (norm_iso(row.get(iso_col, "")),
                   norm_date(row.get(date_col, "")))
            if key not in ref_keys:
                violations.append(row)
                missing_keys.add(key)

        # Optional outputs
        if violations_out_csv:
            with open(violations_out_csv, "w", newline="", encoding="utf-8") as fo:
                w = csv.DictWriter(fo, fieldnames=rf.fieldnames)
                w.writeheader()
                for r in violations:
                    w.writerow(r)

        if missing_keys_out_csv:
            with open(missing_keys_out_csv, "w", newline="", encoding="utf-8") as fo:
                w = csv.DictWriter(fo, fieldnames=[iso_col, date_col])
                w.writeheader()
                for iso, d in sorted(missing_keys):
                    # If you normalized iso to lower, you can emit as-is or keep original case by choice.
                    w.writerow({iso_col: iso, date_col: d})

    return len(violations), len(missing_keys)


# --------------------------
# Example (remove or adapt):
bad_rows, missing_keys = check_fk_iso_date(
    fact_csv="final_vaccine_name.csv",               # child table with FK (isoCode,date)
    ref_csv="ref_vaccine.csv",                # parent table with PK/unique (isoCode,date)
    violations_out_csv="fk_violations_rows.csv",
    missing_keys_out_csv="fk_missing_keys.csv"
)
print(f"Violating rows: {bad_rows} | Distinct missing keys: {missing_keys}")

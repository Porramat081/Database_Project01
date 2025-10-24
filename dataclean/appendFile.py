import csv
from typing import Dict, Optional, Tuple, Set

def append_missing_keys_to_ref(
    ref_csv: str,                 # parent/reference CSV to append into
    violations_csv: str,          # child rows that failed FK (from earlier check)
    iso_col: str = "isoCode",
    date_col: str = "date",
    extra_defaults: Optional[Dict[str, str]] = None,  # defaults for the extra columns
    encoding: str = "utf-8",
) -> int:
    """
    Append unique (isoCode, date) pairs from violations_csv into ref_csv.
    The ref_csv may have extra columns; those columns are filled with "" by default,
    or values from extra_defaults if provided.

    Returns the number of rows appended.
    """
    # 1) Load reference header + existing keys
    with open(ref_csv, newline="", encoding=encoding) as fr:
        rr = csv.DictReader(fr)
        if not rr.fieldnames:
            raise ValueError(f"No header in ref_csv: {ref_csv}")
        header = rr.fieldnames
        if iso_col not in header or date_col not in header:
            raise KeyError(f"ref_csv must contain '{iso_col}' and '{date_col}'. Found: {header}")
        ref_keys: Set[Tuple[str, str]] = set()
        for row in rr:
            ref_keys.add(((row.get(iso_col, "") or "").strip(),
                          (row.get(date_col, "") or "").strip()))

    # 2) Collect distinct missing keys from violations CSV
    missing_keys: Set[Tuple[str, str]] = set()
    with open(violations_csv, newline="", encoding=encoding) as fv:
        rv = csv.DictReader(fv)
        if iso_col not in (rv.fieldnames or []) or date_col not in rv.fieldnames:
            raise KeyError(f"violations_csv must contain '{iso_col}' and '{date_col}'. Found: {rv.fieldnames}")
        for row in rv:
            key = ((row.get(iso_col, "") or "").strip(),
                   (row.get(date_col, "") or "").strip())
            if key and key not in ref_keys:
                missing_keys.add(key)

    if not missing_keys:
        return 0  # nothing to append

    # 3) Prepare defaults for extra columns
    extra_defaults = extra_defaults or {}
    # All columns in ref header except iso/date are "extra"
    extra_cols = [c for c in header if c not in (iso_col, date_col)]

    # 4) Append rows to the reference CSV (no header)
    appended = 0
    with open(ref_csv, "a", newline="", encoding=encoding) as fa:
        w = csv.DictWriter(fa, fieldnames=header)
        # don't writeheader() when appending
        for iso, d in sorted(missing_keys):
            out_row = {c: "" for c in header}
            out_row[iso_col] = iso
            out_row[date_col] = d
            for c in extra_cols:
                out_row[c] = extra_defaults.get(c, "")
            w.writerow(out_row)
            appended += 1

    return appended

# -----------------------
# Example:
# appended = append_missing_keys_to_ref(
#     ref_csv="reference.csv",
#     violations_csv="fk_violations_rows.csv",
#     iso_col="isoCode",
#     date_col="date",
#     extra_defaults={
#         # Optional: provide defaults for the 4 extra columns in reference
#         # "col3": "",
#         # "col4": "",
#         # "col5": "",
#         # "col6": "",
#     }
# )
# print(f"Appended {appended} new reference rows.")

append_missing_keys_to_ref(ref_csv="clean_final_vaccination.csv",violations_csv="fk_violations_rows.csv", extra_defaults={
        Optional: {
        "col3": "",
        "col4": "",
        "col5": "",
        "col6": "",
 }})
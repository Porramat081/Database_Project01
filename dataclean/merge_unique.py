import csv

def merge_unique_by_key(a_csv: str, b_csv: str, out_csv: str,
                        key_cols = ("location", "date", "vaccine"),
                        encoding="utf-8"):
    """Merge A and B, keeping only unique (isoCode,date,vaccine)."""
    seen = set()

    with open(a_csv, newline="", encoding=encoding) as fa, \
         open(b_csv, newline="", encoding=encoding) as fb, \
         open(out_csv, "w", newline="", encoding=encoding) as fo:

        ra = csv.DictReader(fa)
        rb = csv.DictReader(fb)

        # Basic schema check
        if ra.fieldnames != rb.fieldnames:
            raise ValueError(f"Schemas differ.\nA: {ra.fieldnames}\nB: {rb.fieldnames}")

        # Ensure keys exist
        for k in key_cols:
            if k not in ra.fieldnames:
                raise KeyError(f"Missing key column '{k}'")

        w = csv.DictWriter(fo, fieldnames=ra.fieldnames)
        w.writeheader()

        def emit_rows(reader):
            for row in reader:
                key = tuple((row.get(k, "") or "").strip() for k in key_cols)
                if key in seen:
                    continue
                seen.add(key)
                w.writerow(row)

        emit_rows(ra)
        emit_rows(rb)

merge_unique_by_key("merge_select_single.csv","vaccine_selection.csv","out_select_vaccine.csv")
import csv

def dedupe_by_iso_date_no_pandas(input_csv, output_csv,
                                 iso_col="isoCode", date_col="date",
                                 case_insensitive_iso=True, strip_ws=True):
    def norm_iso(v: str) -> str:
        if v is None: return ""
        v = v.strip() if strip_ws else v
        return v.lower() if case_insensitive_iso else v

    def norm_date(v: str) -> str:
        if v is None: return ""
        return v.strip() if strip_ws else v

    seen = set()
    with open(input_csv, newline="", encoding="utf-8") as f_in, \
         open(output_csv, "w", newline="", encoding="utf-8") as f_out:
        r = csv.DictReader(f_in)
        if iso_col not in (r.fieldnames or []) or date_col not in r.fieldnames:
            raise KeyError(f"Missing '{iso_col}' or '{date_col}' in header: {r.fieldnames}")

        w = csv.DictWriter(f_out, fieldnames=r.fieldnames)
        w.writeheader()

        for row in r:
            key = (norm_iso(row.get(iso_col, "")), norm_date(row.get(date_col, "")))
            if key in seen:
                continue  # skip later duplicates
            seen.add(key)
            w.writerow(row)

dedupe_by_iso_date_no_pandas("final_vaccination_mapped.csv","clean_final_vaccination.csv")
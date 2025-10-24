import csv

def explode_multivalue_column(input_csv: str, output_csv: str,
                              column_name: str = "vaccine", sep: str = ",",
                              trim_spaces: bool = True,
                              drop_empty: bool = True):
    """
    Read input_csv and write output_csv where `column_name` is split on `sep`
    and each value gets its own row. Other columns are duplicated.
    """
    with open(input_csv, newline="", encoding="utf-8") as fin, \
         open(output_csv, "w", newline="", encoding="utf-8") as fout:
        r = csv.DictReader(fin)
        if column_name not in (r.fieldnames or []):
            raise KeyError(f"Column '{column_name}' not in {r.fieldnames}")

        w = csv.DictWriter(fout, fieldnames=r.fieldnames)
        w.writeheader()

        for row in r:
            raw = row.get(column_name, "")
            parts = raw.split(sep) if raw is not None else []
            for p in parts:
                v = p.strip() if trim_spaces else p
                if drop_empty and (v is None or v == ""):
                    continue
                out_row = dict(row)
                out_row[column_name] = v
                w.writerow(out_row)

explode_multivalue_column("merge_select.csv","merge_select_single.csv")
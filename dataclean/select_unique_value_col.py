import csv

def unique_one_column_with_header(input_csv: str, output_csv: str):
    with open(input_csv, newline="", encoding="utf-8") as f_in, \
         open(output_csv, "w", newline="", encoding="utf-8") as f_out:
        r = csv.DictReader(f_in)
        if not r.fieldnames or len(r.fieldnames) != 1:
            raise ValueError(f"Expected exactly 1 column, got: {r.fieldnames}")
        col = r.fieldnames[0]

        seen = set()
        uniques = []
        for row in r:
            val = (row.get(col) or "").strip()
            if val not in seen:
                seen.add(val)
                uniques.append(val)

        w = csv.writer(f_out)
        w.writerow([col])           # keep original header
        for v in uniques:
            w.writerow([v])

unique_one_column_with_header("exact_state.csv","unique_state.csv")
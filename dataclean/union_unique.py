import csv

def union_keep_A_and_new_from_B_no_pandas(a_csv, b_csv, out_csv):
    final_cols = ["isoCode", "countryName", "sourceName", "defaultUrl"]

    # Load A and write header; track seen keys
    seen = set()
    with open(out_csv, "w", newline="", encoding="utf-8") as f_out:
        w = csv.DictWriter(f_out, fieldnames=final_cols)
        w.writeheader()

        # Write A first
        with open(a_csv, newline="", encoding="utf-8") as f_a:
            ra = csv.DictReader(f_a)
            for row in ra:
                iso = (row.get("isoCode") or "").strip()
                country = (row.get("countryName") or "").strip()
                key = (iso, country)
                if key not in seen:
                    seen.add(key)
                    w.writerow({
                        "isoCode": iso,
                        "countryName": country,
                        "sourceName": row.get("sourceName", ""),
                        "defaultUrl": row.get("defaultUrl", "")
                    })

        # Append new rows from B (with empty sourceName/defaultUrl)
        with open(b_csv, newline="", encoding="utf-8") as f_b:
            rb = csv.DictReader(f_b)
            for row in rb:
                iso = (row.get("isoCode") or "").strip()
                country = (row.get("countryName") or "").strip()
                key = (iso, country)
                if key not in seen:
                    seen.add(key)
                    w.writerow({
                        "isoCode": iso,
                        "countryName": country,
                        "sourceName": "",
                        "defaultUrl": ""
                    })


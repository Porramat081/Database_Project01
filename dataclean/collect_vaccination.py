import csv

def union_keep_A_and_new_from_B_no_pandas(a_csv, b_csv, out_csv):
    final_cols = ["location", "date" ,"people_vaccinated","people_fully_vaccinated","total_boosters", "source_url"]

    # Load A and write header; track seen keys
    seen = set()
    with open(out_csv, "w", newline="", encoding="utf-8") as f_out:
        w = csv.DictWriter(f_out, fieldnames=final_cols)
        w.writeheader()

        # Write A first
        with open(a_csv, newline="", encoding="utf-8") as f_a:
            ra = csv.DictReader(f_a)
            for row in ra:
                location = (row.get("location") or "").strip()
                date = (row.get("date") or "").strip()
                people_vaccinated = (row.get("people_vaccinated") or "").strip()
                people_fully_vaccinated = (row.get("people_fully_vaccinated") or "").strip()
                total_boosters = (row.get("total_boosters") or "").strip()
                key = (location, date,people_vaccinated,people_fully_vaccinated,total_boosters)
                if key not in seen:
                    seen.add(key)
                    w.writerow({
                        "location": location,
                        "date": date,
                        "people_vaccinated": people_vaccinated,
                        "people_fully_vaccinated": people_fully_vaccinated,
                        "total_boosters": total_boosters,
                        "source_url": row.get("source_url", "")
                    })

        # Append new rows from B (with empty sourceName/defaultUrl)
        with open(b_csv, newline="", encoding="utf-8") as f_b:
            rb = csv.DictReader(f_b)
            for row in rb:
                location = (row.get("location") or "").strip()
                date = (row.get("date") or "").strip()
                people_vaccinated = (row.get("people_vaccinated") or "").strip()
                people_fully_vaccinated = (row.get("people_fully_vaccinated") or "").strip()
                total_boosters = (row.get("total_boosters") or "").strip()
                key = (location, date,people_vaccinated,people_fully_vaccinated,total_boosters)
                if key not in seen:
                    seen.add(key)
                    w.writerow({
                         "location": location,
                        "date": date,
                        "people_vaccinated": people_vaccinated,
                        "people_fully_vaccinated": people_fully_vaccinated,
                        "total_boosters": total_boosters,
                        "source_url": ""
                    })

union_keep_A_and_new_from_B_no_pandas("exact_merge.csv","exact_vaccination.csv","final_vaccination_merged.csv")
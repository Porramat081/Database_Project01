import csv

def unique_values_from_column(input_csv: str,
                              column_name: str,
                              *,
                              case_insensitive: bool = False,
                              strip_ws: bool = True) -> list[str]:
    """
    Return unique values from `column_name`, preserving first-seen order.
    """
    def norm(s: str) -> str:
        if s is None:
            return ""
        s2 = s.strip() if strip_ws else s
        return s2.lower() if case_insensitive else s2

    seen = set()
    uniques = []
    with open(input_csv, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        if column_name not in (r.fieldnames or []):
            raise KeyError(f"Column '{column_name}' not found. Available: {r.fieldnames}")
        for row in r:
            raw = row.get(column_name, "")
            key = norm(raw)
            if key not in seen:
                seen.add(key)
                uniques.append(raw.strip() if strip_ws else raw)
    return uniques

# Example:
vals = unique_values_from_column("vaccinations-by-age-group.csv", "age_group")

# print(vals)

def write_uniques_to_csv(values: list[str], output_csv: str, header: str = "unique_values"):
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([header])
        for v in values:
            w.writerow([v])

# Example:
write_uniques_to_csv(vals, "unique_age_group.csv", header="ageRange")

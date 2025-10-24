import csv

def map_location_to_iso_no_pandas(input_a, input_b, output_csv,
                                  a_location_col="location",
                                  b_location_col="countryName",
                                  b_iso_col="isoCode"):
    # Build a lookup dict from B: normalized location -> isoCode
    def norm(s): return s.strip().lower()

    with open(input_b, newline="", encoding="utf-8") as fb:
        rb = csv.DictReader(fb)
        lookup = {}
        for row in rb:
            loc = row.get(b_location_col, "")
            iso = row.get(b_iso_col, "")
            if loc:
                key = norm(loc)
                # keep first occurrence; change to always overwrite if needed
                lookup.setdefault(key, iso)

    with open(input_a, newline="", encoding="utf-8") as fa, \
         open(output_csv, "w", newline="", encoding="utf-8") as fo:
        ra = csv.DictReader(fa)
        fieldnames = ra.fieldnames or []
        if a_location_col not in fieldnames:
            raise KeyError(f"Column '{a_location_col}' not found in A. Got: {fieldnames}")

        wa = csv.DictWriter(fo, fieldnames=fieldnames)
        wa.writeheader()

        for row in ra:
            loc = row.get(a_location_col, "")
            mapped = lookup.get(norm(loc), "")
            # Replace with isoCode (leave blank if no match)
            row[a_location_col] = mapped if mapped else row[a_location_col]  # or "" to force blanks
            # To drop unmatched rows instead:
            # if not mapped: continue
            wa.writerow(row)

# Example:
map_location_to_iso_no_pandas("vacAge.csv", "country.csv", "A_mapped.csv")

import pandas as pd

def find_missing_keys(first_csv, second_csv, out_csv=None):
    # Read
    df1 = pd.read_csv(first_csv, dtype=str)
    df2 = pd.read_csv(second_csv, dtype=str)

    # Normalise keys
    for c in ["isoCode", "date"]:
        df1[c] = df1[c].str.strip()
        df2[c] = df2[c].str.strip()

    # Treat (isoCode,date) as primary key in first
    pk = ["isoCode", "date"]
    pk_first = df1[pk].drop_duplicates()

    # Anti-join: keys in second not present in first
    violations = (
        df2.merge(pk_first, on=pk, how="left", indicator=True)
           .query('_merge == "left_only"')
           .drop(columns="_merge")
    )

    if out_csv:
        violations.to_csv(out_csv, index=False)

    # Also return just the distinct missing keys if you want
    missing_keys = violations[pk].drop_duplicates()

    print(f"Missing key rows from second: {len(violations)}")
    return violations, missing_keys

# Example:
violations, missing_keys = find_missing_keys("vaccination/merged.csv", "ageGroup/output_selection.csv", out_csv="fk_violations_rows.csv")
#missing_keys.to_csv("fk_violations_keys.csv", index=False)

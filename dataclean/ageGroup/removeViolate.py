import pandas as pd

def remove_violations_from_second(second_csv, violations_csv, out_csv=None, in_place=False):
    # Read
    df2 = pd.read_csv(second_csv, dtype=str)
    dfv = pd.read_csv(violations_csv, dtype=str)

    # Normalise keys
    for c in ["isoCode", "date"]:
        df2[c] = df2[c].str.strip()
        dfv[c] = dfv[c].str.strip()

    # We only need the distinct violating keys
    keys = ["isoCode", "date"]
    bad_keys = dfv[keys].drop_duplicates()

    # Anti-join: keep rows in df2 whose key is NOT in bad_keys
    cleaned = (
        df2.merge(bad_keys, on=keys, how="left", indicator=True)
           .query('_merge == "left_only"')
           .drop(columns="_merge")
    )

    # Save
    if in_place:
        cleaned.to_csv(second_csv, index=False)
    else:
        out_csv = out_csv or "second_cleaned.csv"
        cleaned.to_csv(out_csv, index=False)
    return cleaned

# Example:
remove_violations_from_second("ageGroup/output_selection.csv", "ageGroup/fk_violations_rows.csv", in_place=False)

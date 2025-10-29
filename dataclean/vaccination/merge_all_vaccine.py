import pandas as pd

def merge_keep_first(first_csv, second_csv, out_csv):
    # Read
    df1 = pd.read_csv(first_csv)
    df2 = pd.read_csv(second_csv)

    # Normalise join keys (avoid whitespace/type mismatches)
    for c in ["isoCode", "date"]:
        df1[c] = df1[c].astype(str).str.strip()
        df2[c] = df2[c].astype(str).str.strip()

    # Ensure there's only one (isoCode,date) in the first file (keep first)
    df1 = df1.drop_duplicates(subset=["isoCode", "date"], keep="first")

    # Anti-join: rows in df2 not present in df1 on (isoCode,date)
    keys = ["isoCode", "date"]
    new_rows = df2.merge(
        df1[keys].drop_duplicates(),
        on=keys, how="left", indicator=True
    ).loc[lambda x: x["_merge"] == "left_only"].drop(columns="_merge")

    # Combine, preserving df1’s column order
    out = pd.concat([df1, new_rows[df1.columns]], ignore_index=True)

    # (Optional) final de-dupe just in case
    out = out.drop_duplicates(subset=keys, keep="first")

    out.to_csv(out_csv, index=False)

# Example:
merge_keep_first("country/output2.csv", "vaccination/output3_url.csv", "vaccination/merged.csv")

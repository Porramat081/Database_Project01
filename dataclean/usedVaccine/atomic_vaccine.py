import pandas as pd

def atomize_multivalue_column(
    csv_in: str,
    col: str,                  # the multi-valued column name
    csv_out: str,
    sep: str = ",",
    drop_empty: bool = True,
    dedupe_rows: bool = True
):
    """
    Reads csv_in, splits column `col` on `sep`, explodes into atomic rows, 
    strips whitespace, optionally drops empties and duplicate rows, and writes to csv_out.
    """
    df = pd.read_csv(csv_in, dtype=str).fillna("")

    # Split into lists (respect simple comma-separated; if you have embedded commas inside quotes,
    # make sure the original CSV is properly quoted—pd.read_csv will handle that)
    df[col] = df[col].astype(str).str.split(sep)

    # Explode to one value per row
    out = df.explode(col, ignore_index=True)

    # Trim whitespace around each value
    out[col] = out[col].astype(str).str.strip()

    # Optionally drop empty/blank values
    if drop_empty:
        out = out.loc[out[col].ne("")]

    # Optionally de-duplicate exact duplicate rows
    if dedupe_rows:
        out = out.drop_duplicates(ignore_index=True)

    out.to_csv(csv_out, index=False)
    return out

# Example:
# Suppose columns: isoCode,date,vaccines
# vaccines might be like: "Pfizer, Moderna , AstraZeneca"
atomize_multivalue_column("usedVaccine/output2.csv", "vaccine", "usedVaccine/vaccines_atomic.csv")

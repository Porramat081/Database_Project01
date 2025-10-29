import pandas as pd

# Read the original CSV
df = pd.read_csv('country/output.csv')

# Select only the columns you want (in the order you want)
df_filtered = df[["isoCode" , "date","people_vaccinated","people_fully_vaccinated","total_boosters" , "source_url"]]

# Save the new CSV
df_filtered.to_csv('country/output2.csv', index=False)

print("✅ Created 'output.csv' with only columns (b, a, d).")
import pandas as pd

# Read the original CSV
df = pd.read_csv('usedVaccine/output.csv')

# Select only the columns you want (in the order you want)
# date,vaccine,total_vaccinations,isoCode
df_filtered = df[["isoCode","date", "vaccine"]]

# Save the new CSV
df_filtered.to_csv('usedVaccine/output2.csv', index=False)

print("✅ Created 'output.csv' with only columns (b, a, d).")
import pandas as pd

# Read the original CSV
df = pd.read_csv('vaccination/vaccinations.csv')

# Select only the columns you want (in the order you want)
df_filtered = df[["iso_code" , "date","people_vaccinated","people_fully_vaccinated","total_boosters"]]

# Save the new CSV
df_filtered.to_csv('vaccination/output1.csv', index=False)

print("✅ Created 'output.csv' with only columns (b, a, d).")

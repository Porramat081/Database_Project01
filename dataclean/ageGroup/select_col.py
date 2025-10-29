import pandas as pd

# Read the original CSV
df = pd.read_csv('ageGroup/output_map.csv')

# Select only the columns you want (in the order you want)
df_filtered = df[["isoCode" ,"date" , "age_group", "people_vaccinated_per_hundred","people_fully_vaccinated_per_hundred" , "people_with_booster_per_hundred"]]

# Save the new CSV
df_filtered.to_csv('ageGroup/output_selection.csv', index=False)

print("✅ Created 'output.csv' with only columns (b, a, d).")

# date,location,total_vaccinations,total_distributed,people_vaccinated,people_fully_vaccinated_per_hundred,total_vaccinations_per_hundred,people_fully_vaccinated,people_vaccinated_per_hundred,distributed_per_hundred,daily_vaccinations_raw,daily_vaccinations,daily_vaccinations_per_million,share_doses_used,total_boosters,total_boosters_per_hundred
# 2021-01-12,Alabama,78134.0,377025.0,70861.0,0.15,1.59,7270.0,1.45,7.69,,,,0.207,,

import pandas as pd

# Read the original CSV
df = pd.read_csv('vaccineState/output2.csv')

# Select only the columns you want (in the order you want)
df_filtered = df[["isoCode","location","date" , "total_distributed", "people_vaccinated","people_fully_vaccinated" , "total_boosters"]]

# Save the new CSV
df_filtered.to_csv('vaccineState/output3.csv', index=False)

print("✅ Created 'output.csv' with only columns (b, a, d).")

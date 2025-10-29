import pandas as pd

# Read the original CSV
df = pd.read_csv('location/locations.csv')

# Select only the columns you want (in the order you want)
df_filtered = df[["iso_code" , "location","source_name","source_website"]]

# Save the new CSV
df_filtered.to_csv('location/output.csv', index=False)

print("✅ Created 'output.csv' with only columns (b, a, d).")

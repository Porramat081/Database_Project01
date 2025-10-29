import pandas as pd

# Step 1: Read the original CSV
df = pd.read_csv('sourceCountry/ohm_source_country.csv')

# Step 2: Remove duplicate rows in each column separately

names = df[['source_name']].drop_duplicates()
urls = df[['source_website']].drop_duplicates()

# Step 3: Save them into two separate CSV files
names.to_csv('names.csv', index=False)
urls.to_csv('urls.csv', index=False)

print("✅ Done! Created 'names.csv' and 'urls.csv' without duplicates.")

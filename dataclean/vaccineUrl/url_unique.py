import pandas as pd

# Step 1: Read the original CSV
df = pd.read_csv('vaccination/merged.csv')

# Step 2: Remove duplicate rows in each column separately

state_names = df[['url']].drop_duplicates()

# Step 3: Save them into two separate CSV files
state_names.to_csv('vaccineUrl/url.csv', index=False)

print("✅ Done! Created 'names.csv' and 'urls.csv' without duplicates.")
import pandas as pd

# Step 1: Read your CSV
df = pd.read_csv('vaccination/output1.csv')

# Step 2: Remove rows where isoCode starts with 'OWID'
df_cleaned = df[~df['iso_code'].str.startswith('OWID', na=False)]

# Step 3: Save the cleaned data
df_cleaned.to_csv('vaccination/output2.csv', index=False)

print("✅ Removed rows where isoCode starts with 'OWID'. Saved as 'output.csv'.")

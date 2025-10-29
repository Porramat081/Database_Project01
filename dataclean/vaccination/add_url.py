import pandas as pd

# Read the original CSV
df = pd.read_csv('vaccination/output2.csv')

# Add new column with constant value
df['url'] = ""

# Save to a new CSV
df.to_csv('output3_url.csv', index=False)

print("✅ Added column 'isoCode' with value 'USA' and saved as 'output.csv'.")
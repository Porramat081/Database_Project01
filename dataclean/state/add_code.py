import pandas as pd

# Read the original CSV
df = pd.read_csv('state/stateName.csv')

# Add new column with constant value
df['isoCode'] = 'USA'

# Save to a new CSV
df.to_csv('output.csv', index=False)

print("✅ Added column 'isoCode' with value 'USA' and saved as 'output.csv'.")

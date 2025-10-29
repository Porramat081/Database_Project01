import pandas as pd

# Read the original CSV
df = pd.read_csv('vaccineState/output.csv')

# Add new column with constant value
df['isoCode'] = 'USA'

# Save to a new CSV
df.to_csv('output2.csv', index=False)

print("✅ Added column 'isoCode' with value 'USA' and saved as 'output.csv'.")
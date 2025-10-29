import pandas as pd

# Step 1: Read both CSV files
main_df = pd.read_csv('ageGroup/input.csv')
country_df = pd.read_csv('location/output.csv')

# Step 2: Merge them on the 'location' column
merged_df = main_df.merge(country_df, on='location', how='left')

# Step 3: Drop the old location column and rearrange (optional)
merged_df = merged_df.drop(columns=['location'])
# Or rename isoCode column to replace location:
# merged_df = merged_df.rename(columns={'isoCode': 'location'})

# Step 4: Save the result
merged_df.to_csv('ageGroup/output_map.csv', index=False)

print("✅ Merged successfully! 'location' replaced with matching isoCode.")
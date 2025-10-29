import pandas as pd
import glob

# Step 1: List all CSV files (you can adjust the path or pattern)
# Example: if your files are named data1.csv, data2.csv, ..., data6.csv
csv_files = ["country/Argentina.csv" , "country/Australia.csv" , "country/Canada.csv" , "country/Greece.csv" , "country/India.csv" , "country/United States.csv"]

# Step 2: Read and combine all CSVs into one DataFrame
df_list = [pd.read_csv(file) for file in csv_files]
merged_df = pd.concat(df_list, ignore_index=True)

# Step 3: Select only the desired columns
selected_columns = ['location', 'date', 'vaccine']
merged_df = merged_df[selected_columns]

# Step 4: Save the merged and filtered data
merged_df.to_csv('merged_output.csv', index=False)

print("✅ Merged 6 CSV files and saved 'merged_output.csv' with selected columns.")

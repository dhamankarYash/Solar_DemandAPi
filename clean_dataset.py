import pandas as pd

# Define paths
raw_file = 'data/efinal_consumption.csv'   # ✅ your input file
clean_file = 'data/final_consumption.csv'  # ✅ output file

# Load raw data
df = pd.read_csv(raw_file)

# Rename columns for consistency
df = df.rename(columns={
    'srcStateName': 'State',
    'Electricity consumption by ultimate consumers': 'Consumption',
    'YearCode': 'Year'
})

# Keep only relevant columns
df = df[['State', 'Year', 'Consumption']]

# Clean values: strip whitespace and standardize title case
df['State'] = df['State'].str.strip().str.title()

# Save cleaned dataset
df.to_csv(clean_file, index=False)

print("✅ Saved clean dataset to:", clean_file)

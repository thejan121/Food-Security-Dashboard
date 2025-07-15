import pandas as pd

# Load the Excel file (adjust the path if needed)
file_path = r'C:\Users\USER\Downloads\production2.xlsx'
raw_df = pd.read_excel(file_path, header=None)

# Extract the years and seasons from the first two rows
years = raw_df.iloc[0, 1:].ffill().infer_objects(copy=False).values
seasons = raw_df.iloc[1, 1:].values

# Combine year and season to make proper headers
new_columns = ['District'] + [f"{year} {season}" for year, season in zip(years, seasons)]

# Extract the data starting from the 3rd row
data = raw_df.iloc[2:].copy()
data.columns = new_columns

# Convert to long format
long_df = data.melt(id_vars='District', var_name='Year_Season', value_name='Production')

# Split the Year_Season column into Year and Season
long_df[['Year', 'Season']] = long_df['Year_Season'].str.extract(r'(\d{4})\s+(Yala|Maha)')

# Drop the combined column and remove incomplete rows
long_df = long_df.drop(columns='Year_Season')
long_df = long_df.dropna(subset=['Year', 'Season'])

# Reorder and reset index
long_df = long_df[['District', 'Year', 'Season', 'Production']].reset_index(drop=True)

# Optional: save to a new Excel or CSV file
long_df.to_excel(r'C:\Users\USER\Downloads\production_long_format2.xlsx', index=False)
# long_df.to_csv(r'C:\Users\USER\Downloads\production_long_format.csv', index=False)

print("Conversion complete. File saved as 'production_long_format.xlsx'.")

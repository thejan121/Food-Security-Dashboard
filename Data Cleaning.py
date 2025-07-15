import pandas as pd

# File path
file_path = r'D:\Dashboard\New dash Board\production.xlsx'

# Read all sheet names
xls = pd.ExcelFile(file_path)
sheet_names = xls.sheet_names

# Store all cleaned sheets
all_data = []

for sheet in sheet_names:
    df_raw = pd.read_excel(file_path, sheet_name=sheet, header=None)

    # Drop any rows where first column is NaN (likely empty headers)
    df_raw = df_raw.dropna(subset=[0])

    # Reset index
    df_raw.reset_index(drop=True, inplace=True)

    # Now: first column = district, the rest are values
    # Assume format: district | 2015_Yala | 2015_Maha | 2015_Total | 2016_Yala | ...
    total_columns = df_raw.shape[1]

    # Determine how many Yala/Maha pairs there are (each year = 3 columns)
    num_years = (total_columns - 1) // 3

    # Select only Yala and Maha columns (skip Totals)
    selected_col_indices = [0]  # district
    for i in range(num_years):
        yala_idx = 1 + i * 3
        maha_idx = yala_idx + 1
        selected_col_indices.extend([yala_idx, maha_idx])

    df = df_raw.iloc[:, selected_col_indices]

    # Assign proper column names
    new_columns = ['district']
    start_year = 2015
    for i in range(num_years):
        year = start_year + i
        new_columns.extend([f'{year}_Yala', f'{year}_Maha'])

    df.columns = new_columns

    # Melt to long format
    df_long = df.melt(id_vars='district', var_name='year_season', value_name='production')
    df_long[['year', 'season']] = df_long['year_season'].str.split('_', expand=True)
    df_long.drop(columns='year_season', inplace=True)

    # Optional: Add crop name from sheet
    df_long['crop'] = sheet

    all_data.append(df_long)

# Combine all sheets
final_df = pd.concat(all_data, ignore_index=True)

# Save to CSV
final_df.to_csv(r'D:\Dashboard\New dash Board\all_production_long.csv', index=False)

print("✅ All sheets processed successfully — long format (Yala/Maha only).")

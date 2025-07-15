import pandas as pd
from datetime import datetime, timedelta

#Change File Name and Path
file_path = r"C:\Users\USER\Downloads\KFP.xlsx"
df = pd.read_excel(file_path)

df['Date'] = pd.to_datetime(df['Date'])

#Change date range (2015-01-01 to 2019-12-31)
start_date = datetime(2015, 1, 1)
end_date = datetime(2019, 12, 31)
all_dates = pd.date_range(start=start_date, end=end_date, freq='D')

complete_df = pd.DataFrame({'Date': all_dates})


complete_df = complete_df.merge(df, on='Date', how='left')

complete_df['Price'] = complete_df['Price'].ffill()

#Save as a new file
output_path = r"C:\Users\USER\Downloads\Final KFP.xlsx"
complete_df.to_excel(output_path, index=False)

print(f"Completed file saved to {output_path}")

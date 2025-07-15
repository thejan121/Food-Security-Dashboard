import pandas as pd

# Load the CSV file
file_path = r"C:\Users\USER\Downloads\date.csv"
df = pd.read_csv(file_path, header=None, names=["OriginalDate", "Value"])

# Convert the 'OriginalDate' column to the format M/D/YYYY
df["FormattedDate"] = pd.to_datetime(df["OriginalDate"]).dt.strftime("%-m/%-d/%Y")

# Print the result
print(df[["OriginalDate", "FormattedDate"]])

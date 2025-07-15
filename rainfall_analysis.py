import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# === Step 1: Load the Data ===
file_path = r'C:\Users\USER\Downloads\Rainfall data.xlsx'
df = pd.read_excel(file_path)

print("Columns in the dataset:")
print(df.columns)

# === Step 2: Data Cleaning ===
# Assuming the first column is Date and the rest are station names
df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Optional: Fill missing values with station-wise monthly average
df = df.apply(lambda x: x.fillna(x.mean()), axis=0)

# === Step 3: Data Visualization ===
plt.figure(figsize=(15, 7))
for station in df.columns[:5]:  # Adjust [:5] to [:25] for all stations
    plt.plot(df.index, df[station], label=station)
plt.title('Monthly Rainfall Trends (Sample Stations)')
plt.xlabel('Date')
plt.ylabel('Rainfall (mm)')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# === Step 4: Forecast 2025 Rainfall ===
forecast_results = {}

for station in df.columns:
    # Fit a seasonal Holt-Winters model (monthly seasonality = 12)
    model = ExponentialSmoothing(df[station], seasonal='add', seasonal_periods=12)
    model_fit = model.fit()

    # Forecast 12 months for 2025
    forecast = model_fit.forecast(steps=12)
    forecast.index = pd.date_range(start='2025-01-01', periods=12, freq='MS')
    forecast_results[station] = forecast

# === Step 5: Save the Forecast ===
forecast_df = pd.DataFrame(forecast_results)
forecast_df.to_excel(r"C:\Users\USER\Downloads\Rainfall_2025_Predictions.xlsx")

print("✅ Forecast saved as 'Rainfall_2025_Predictions.xlsx' in your Downloads folder.")

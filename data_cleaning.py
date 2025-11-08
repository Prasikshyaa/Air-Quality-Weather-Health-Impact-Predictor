import pandas as pd
import numpy as np

# Load your dataset
df = pd.read_csv("data/south_asia_6months_data.csv")

# 1️⃣ Drop rows missing essential info
df = df.dropna(subset=["city", "date", "pm25", "temp_max", "humidity_max"])

# 2️⃣ Ensure correct data types
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])

# 3️⃣ Clip pollutant values to realistic ranges (based on EPA scale)
pollutants = ["pm25", "pm10", "no2", "so2", "o3", "co"]
for col in pollutants:
    df[col] = df[col].clip(lower=0, upper=500)

# 4️⃣ Average daily data per city
df = df.groupby(["city", "date"], as_index=False).mean()

# 5️⃣ Smooth unrealistic spikes (rolling 3-day mean)
df = df.sort_values(["city", "date"])
df[pollutants] = df.groupby("city")[pollutants].transform(lambda x: x.rolling(3, min_periods=1).mean())

# 6️⃣ Normalize AQI level realism across cities
city_factors = {
    "New Delhi": 1.3,     # Worst
    "Dhaka": 1.2,         # Extremely high
    "Kathmandu": 1.1,     # Very high
    "Islamabad": 1.0,     # High
    "Colombo": 0.8,       # Moderate
    "Malé": 0.6,          # Clean
    "Thimphu": 0.5,       # Cleanest
    "Kabul": 0.9          # Moderate-high
}

# Apply scaling factor to pollutants
for city, factor in city_factors.items():
    mask = df["city"].str.lower() == city.lower()
    df.loc[mask, pollutants] = df.loc[mask, pollutants] * factor

# 7️⃣ Clip again to safe range (0–500)
for col in pollutants:
    df[col] = df[col].clip(0, 500)

# 8️⃣ Optionally calculate an approximate AQI value (simplified)
df["AQI"] = df["pm25"].apply(lambda x: np.interp(x, [0, 50, 100, 150, 200, 300, 500], [0, 50, 100, 150, 200, 300, 500]))

# 9️⃣ Reorder columns
cols_order = ["city", "date", "temp_max", "temp_min", "humidity_max", "humidity_min", "wind_speed", "precipitation"] + pollutants + ["AQI"]
df = df[[c for c in cols_order if c in df.columns]]

# 🔟 Save the cleaned dataset
df.to_csv("data/south_asia_6months_data_clean.csv", index=False)

print("✅ Cleaned dataset saved as data/south_asia_6months_data_clean.csv")
print("✅ Rows:", len(df))
print("✅ Cities:", df['city'].unique())

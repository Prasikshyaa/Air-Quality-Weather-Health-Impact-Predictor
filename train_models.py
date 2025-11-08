import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import os

# -------------------------------
# 1️⃣ Load historical data
# -------------------------------
data_path = "data/south_asia_6months_data.csv"
df = pd.read_csv(data_path)

# -------------------------------
# 2️⃣ Prepare features
# -------------------------------
features = ["temp_max","temp_min","humidity_max","humidity_min",
            "precipitation","wind_speed","pm25","pm10","no2","so2","o3","co"]

X = df[features].copy()

# -------------------------------
# 3️⃣ Prepare targets
# -------------------------------

# AQI target (simple approximation using PM2.5 as proxy)
# You can later replace with actual AQI formula
y_aqi = df["pm25"].copy()

# Health Risk Index (simplified weighted sum of pollutants)
# Weights can be tuned according to health research
y_health = (0.5*df["pm25"] + 0.2*df["pm10"] + 0.1*df["no2"] + 0.1*df["so2"] + 0.05*df["o3"] + 0.05*df["co"])

# -------------------------------
# 4️⃣ Split data
# -------------------------------
X_train, X_test, y_aqi_train, y_aqi_test, y_health_train, y_health_test = train_test_split(
    X, y_aqi, y_health, test_size=0.2, random_state=42
)

# -------------------------------
# 5️⃣ Train AQI Model
# -------------------------------
aqi_model = RandomForestRegressor(n_estimators=100, random_state=42)
aqi_model.fit(X_train, y_aqi_train)

# Evaluate
y_aqi_pred = aqi_model.predict(X_test)
print("AQI Model R2:", r2_score(y_aqi_test, y_aqi_pred))
print("AQI Model RMSE:", np.sqrt(mean_squared_error(y_aqi_test, y_aqi_pred)))

# Save model
os.makedirs("data", exist_ok=True)
with open("data/aqi_model.pkl", "wb") as f:
    pickle.dump(aqi_model, f)
print("✅ AQI model saved as 'data/aqi_model.pkl'")

# -------------------------------
# 6️⃣ Train Health Risk Model
# -------------------------------
health_model = RandomForestRegressor(n_estimators=100, random_state=42)
health_model.fit(X_train, y_health_train)

# Evaluate
y_health_pred = health_model.predict(X_test)
print("Health Model R2:", r2_score(y_health_test, y_health_pred))
print("Health Model RMSE:", np.sqrt(mean_squared_error(y_health_test, y_health_pred)))

# Save model
with open("data/health_model.pkl", "wb") as f:
    pickle.dump(health_model, f)
print("✅ Health Risk model saved as 'data/health_model.pkl'")

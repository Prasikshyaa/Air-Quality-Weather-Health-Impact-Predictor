# Air Quality, Weather & Health Impact Predictor

## Project Introduction
The **Air Quality, Weather & Health Impact Predictor** is a data-driven web dashboard that provides both real-time and historical insights into air quality, weather conditions, and their impact on public health across South Asian capitals.  

Built using **Python**, **Streamlit**, and **Machine Learning**, this application enables users, policymakers, and researchers to understand environmental patterns through intuitive visualizations and AI-based predictions.

The system leverages public APIs such as **OpenWeatherMap** for live data and integrates trained Random Forest models to predict the **Air Quality Index (AQI)** and a custom **Health Risk Index**, providing actionable insights and safety suggestions for users.

---

## Project Workflow
1. **Data Collection**  
   - Historical air quality and weather data for South Asian capitals are retrieved using OpenWeatherMap APIs and stored in `data/south_asia_6months_data.csv`.  
   - Real-time data is fetched on demand from the OpenWeatherMap API.

2. **Data Cleaning & Preprocessing**  
   - Executed via `data_cleaning.py`, which removes missing values, normalizes pollutant levels, and creates a clean dataset (`south_asia_6months_data_clean.csv`).

3. **Model Training**  
   - `train_models.py` trains two machine learning models:  
     - `aqi_model.pkl` — Predicts Air Quality Index (AQI)  
     - `health_model.pkl` — Predicts Health Risk Index  

4. **Dashboard Visualization (Streamlit App)**  
   - The interactive dashboard is powered by `app.py`.  
   - Displays:  
     - Real-time weather and AQI information  
     - Historical and predicted AQI trends  
     - Health impact summaries  
     - City-wise comparison visualizations  

5. **User Interaction & Insights**  
   - Users can explore real-time conditions, predictions, and color-coded health impact visualizations.  
   - Suggestions are provided for safe outdoor activities based on air quality levels.

---

## Project Structure

```
PYTHON_PROJECT/
├── assets/
│ └── style.css
├── data/
│ ├── weather_latest.csv
│ ├── air_quality_latest.csv
│ ├── aqi_model.pkl
│ ├── health_model.pkl
│ ├── south_asia_6months_data.csv
│ └── south_asia_6months_data_clean.csv
├── notebooks/
│ ├── data_fetch.ipynb
│ └── fetch_historical_data.ipynb
├── app.py
├── data_cleaning.py
├── train_models.py
├── requirement.txt
├── README.md
└── Project_Details.md
```
---

## Author
**Prasikshya Karki — 2025**

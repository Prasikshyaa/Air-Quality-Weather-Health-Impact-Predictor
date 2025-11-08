# 🌏 Air Quality, Weather & Health Impact Predictor

## 📖 Project Introduction
The **Air Quality, Weather & Health Impact Predictor** is a data-driven web dashboard that provides real-time and historical insights into air quality, weather conditions, and their impact on public health across South Asian capitals.  
Built using **Python**, **Streamlit**, and **Machine Learning**, this app helps users, policymakers, and researchers easily understand environmental patterns through intuitive visualizations and AI-based predictions.

The system uses open APIs such as **OpenWeatherMap** for live data and integrates trained Random Forest models to predict **Air Quality Index (AQI)** and a custom **Health Risk Index**, providing personalized insights and safety suggestions for users.

---

## ⚙️ Project Workflow
1. **Data Collection**  
   - Historical air quality and weather data for South Asian capitals are fetched using Openweather Air pollution APIs and stored in `data/south_asia_6months_data.csv`.
   - Real-time updates are retrieved from OpenWeatherMap API.

2. **Data Cleaning & Preprocessing**  
   - Handled by `data_cleaning.py`, which removes missing values, normalizes pollutants, and creates a clean dataset (`south_asia_6months_data_clean.csv`).

3. **Model Training**  
   - `train_models.py` trains two machine learning models:
     - `aqi_model.pkl` — Predicts Air Quality Index  
     - `health_model.pkl` — Predicts Health Risk Index

4. **Dashboard Visualization (Streamlit App)**  
   - `app.py` powers the interactive dashboard.
   - Displays:
     - Real-time weather and AQI information  
     - Historical and predicted AQI trends  
     - Health impact summaries  
     - City-wise comparison visualizations

5. **User Interaction & Insights**  
   - Users can explore real-time conditions, predictions, and color-coded health impact visualizations.
   - Suggestions are provided for safe outdoor activities based on air quality levels.

---

## 📁 Project Structure

PYTHON_PROJECT/
│
├── assets/
│ └── style.css # Custom styling for the Streamlit app
│
├── data/
│ ├── air_quality_latest.csv
│ ├── weather_latest.csv
│ ├── aqi_model.pkl
│ ├── health_model.pkl
│ ├── south_asia_6months_data.csv
│ └── south_asia_6months_data_clean.csv
│
├── notebooks/
│ ├── data_fetch.ipynb
│ └── fetch_historical_data.ipynb
│
├── app.py # Main Streamlit application
├── data_cleaning.py # Data preprocessing and cleaning script
├── train_models.py # Model training script
├── requirements.txt # Project dependencies
├── Documentation.md # Detailed technical documentation
└── README.md # Project overview and usage guide

---

## 👩‍💻 Author
**Prasikshya Karki — 2025**
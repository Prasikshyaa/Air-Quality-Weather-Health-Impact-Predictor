# Air Quality Prediction and Analysis of South Asian Capitals

---

## 1. Introduction

This project focuses on analyzing and predicting air quality trends for the capital cities of South Asia.  
The goal is to provide data-driven insights into pollution levels, weather correlations, and health risks associated with air quality index (AQI) variations.

It combines historical environmental datasets and machine learning models to estimate future air quality and related health impacts.  
Interactive visual dashboards have been developed to communicate these findings effectively to both technical and non-technical audiences.

---

## 2. Objectives

- To clean, preprocess, and integrate weather and air quality data for nine South Asian capitals.  
- To train predictive models for Air Quality Index (AQI) and Health Risk Index using machine learning.  
- To visualize historical, comparative, and predictive trends across cities.  
- To build an analytical interface using Streamlit for real-time insights and public awareness.

---

## 3. Methodology

### a. Data Collection and Cleaning
- Historical weather and air quality data were collected from open and verified sources.  
- Missing and inconsistent data entries were identified and handled.  
- Extreme pollutant values were smoothed using a **3-day rolling mean**.  
- A scaling factor was applied to normalize pollution severity based on each city’s pollution level.

### b. Model Development
- Two **Random Forest Regressor** models were trained:
  1. **AQI Prediction Model** – estimates future air quality values.  
  2. **Health Risk Model** – predicts the potential health impact from pollutant exposure.  
- Models were trained using an 80/20 data split.  
- Performance was evaluated using **R² Score** and **Root Mean Square Error (RMSE)**.

### c. Visualization and Dashboard
- The dashboard was built using **Streamlit**, with visualizations powered by **Plotly**, **Matplotlib**, and **Altair**.  
- Key components of the app include:
  - Real-time weather and AQI updates  
  - Health index and step-out recommendations  
  - Comparative visualizations for South Asian capitals  
  - Predictive insights on AQI and health impact  

---

## 4. Project Workflow

1. **Data Preparation:** Cleaning and saving datasets using `data_cleaning.py`.  
2. **Model Training:** Building and saving trained models through `train_models.py`.  
3. **Dashboard Visualization:** Using `app.py` to display all analytics and insights.  
4. **Exploration and Testing:** Conducted in Jupyter Notebooks (`notebooks/` directory).

---

## 5. Project Structure

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

## 6. Key Findings and Insights

- **New Delhi** and **Dhaka** recorded the highest pollution levels in South Asia.  
- **Kathmandu** displayed high PM2.5 concentration, largely due to geographical and seasonal factors.  
- **Islamabad** showed moderate but rising pollution trends.  
- **Colombo**, **Malé**, and **Thimphu** maintained clean air quality across the observation period.  
- Weather factors such as temperature and humidity showed minor correlation with AQI variations.  
- Predicted health risk trends validated WHO’s concerns about chronic exposure in polluted cities.

---

## 7. Tools and Technologies Used

- **Programming Language:** Python  
- **Frameworks:** Streamlit, scikit-learn  
- **Visualization Libraries:** Plotly, Matplotlib, Altair  
- **Data Handling:** pandas, NumPy  
- **Environment:** Virtual Environment (venv)  
- **Version Control:** Git and GitHub  

---

## Author

**Prasikshya Karki – 2025**



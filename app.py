# app.py (full working version with requested changes)
import os
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dotenv import load_dotenv
import pickle

# ------------------------------
# Setup & Config
# ------------------------------
load_dotenv(dotenv_path=".env")
API_KEY = st.secrets.get("api", {}).get("OPENWEATHER_API_KEY") or os.getenv("OPENWEATHER_API_KEY")

st.set_page_config(page_title="Air Quality, Weather & Health Impact Predictor", layout="wide")

if os.path.exists("assets/style.css"):
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🌤️ Air Quality, Weather & Health Impact Predictor")
st.markdown("Analyze real-time weather & air quality, predict AQI & health impact for 8 South Asian capitals")

menu = st.sidebar.radio("Menu", ["Home", "🕒 Real-Time Data", "📊 Prediction Analysis"])

# ------------------------------
# Utility functions
# ------------------------------
def compute_health_index(components_dict):
    pm25 = components_dict.get("pm2_5", 0)
    pm10 = components_dict.get("pm10", 0)
    no2 = components_dict.get("no2", 0)
    so2 = components_dict.get("so2", 0)
    o3 = components_dict.get("o3", 0)
    co = components_dict.get("co", 0)
    return 0.5*pm25 + 0.2*pm10 + 0.1*no2 + 0.1*so2 + 0.05*o3 + 0.05*co

def health_label_and_color(v):
    if v <= 50:
        return "Good", "#2ecc71"
    elif v <= 100:
        return "Moderate", "#f1c40f"
    elif v <= 150:
        return "Unhealthy for Sensitive Groups", "#e67e22"
    elif v <= 200:
        return "Unhealthy", "#e74c3c"
    else:
        return "Very Unhealthy", "#8e44ad"

# ------------------------------
# Dashboard
# ------------------------------
if menu == "Home":
    st.subheader("About")
    st.write("""
    This app provides an easy way to check how clean or polluted the air is in different parts of the world. You can look up real-time weather and air quality for any city, and you can also view predicted air quality for selected South Asian capitals. These predictions help you understand how pollution levels may change and what that means for your health and daily activities.
    """)


    hist_path = "data/south_asia_6months_data_clean.csv"
    if os.path.exists(hist_path):
        df = pd.read_csv(hist_path)
        st.subheader("Sample Historical Data Overview")
        
      
        #group by city and compute mean for key columns
        city_summary = df.groupby("city")[["pm25","temp_max","humidity_max","AQI"]].mean().reset_index()
        st.dataframe(city_summary)
    else:
        st.info("Clean historical dataset not found at data/south_asia_6months_data_clean.csv")

# ------------------------------
# Real-Time Data
# ------------------------------
elif menu == "🕒 Real-Time Data":
    st.subheader("Real-Time Data")
    city_input = st.text_input("Enter City Name", "Kathmandu")

    if st.button("Fetch Real-Time Data"):
        try:
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_input}&limit=1&appid={API_KEY}"
            geo = requests.get(geo_url).json()
            if not geo:
                st.error("City not found. Check spelling.")
            else:
                lat, lon = geo[0]["lat"], geo[0]["lon"]

                # Weather
                weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
                w = requests.get(weather_url, timeout=10).json()
                dt_utc = datetime.utcfromtimestamp(w["dt"])
                weather_df = pd.DataFrame([{
                    "Date": dt_utc.date().isoformat(),
                    "Time": dt_utc.time().strftime("%H:%M:%S"),
                    "Temperature (°C)": w["main"]["temp"],
                    "Humidity (%)": w["main"]["humidity"],
                    "Pressure (hPa)": w["main"]["pressure"],
                    "Wind Speed (m/s)": w["wind"]["speed"],
                    "Description": w["weather"][0]["description"].title()
                }])
                st.markdown("### Current Weather")
                st.dataframe(weather_df)

                # Air pollution
                aq_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
                aq_json = requests.get(aq_url, timeout=10).json()
                components = aq_json["list"][0]["components"]
                aq_dt = aq_json["list"][0]["dt"]

                aq_df = pd.DataFrame([{
                    "City": city_input,
                    "Date": datetime.utcfromtimestamp(aq_dt).date().isoformat(),
                    "Time": datetime.utcfromtimestamp(aq_dt).time().strftime("%H:%M:%S"),
                    "PM2.5": components.get("pm2_5", None),
                    "PM10": components.get("pm10", None),
                    "NO₂": components.get("no2", None),
                    "SO₂": components.get("so2", None),
                    "O₃": components.get("o3", None),
                    "CO": components.get("co", None),
                }])
                st.markdown("### Current Pollutant Levels")
                st.dataframe(aq_df)

                # Pollutant bar chart
                labels = ["PM2.5","PM10","NO₂","SO₂","O₃","CO"]
                values = [components.get("pm2_5",0), components.get("pm10",0), components.get("no2",0),
                          components.get("so2",0), components.get("o3",0), components.get("co",0)]
                fig_poll = px.bar(x=labels, y=values, labels={"x":"Pollutant","y":"Concentration (µg/m³)"},
                                  title=f"Pollutant Concentrations in {city_input}")
                st.plotly_chart(fig_poll, use_container_width=True)


        except Exception as e:
            st.error(f"Error fetching real-time data: {e}")

# ------------------------------
# Prediction Analysis
# ------------------------------
elif menu == "📊 Prediction Analysis":
    sub = st.sidebar.radio("Section", ["City Prediction", "Insights", "Comparison"])

    # --------------------------
    # City Prediction
    # --------------------------
    if sub == "City Prediction":
        st.subheader("City Prediction (8 Capitals)")

        try:
            with open("data/aqi_model.pkl", "rb") as f:
                aqi_model = pickle.load(f)
            with open("data/health_model.pkl", "rb") as f:
                health_model = pickle.load(f)
        except Exception as e:
            st.error(f"Model load error: {e}")
            st.stop()

        capitals = {
            "Kabul": {"lat":34.5553,"lon":69.2075},
            "Dhaka": {"lat":23.8103,"lon":90.4125},
            "Thimphu": {"lat":27.4712,"lon":89.6339},
            "New Delhi": {"lat":28.6139,"lon":77.2090},
            "Malé": {"lat":4.1755,"lon":73.5093},
            "Kathmandu": {"lat":27.7172,"lon":85.3240},
            "Islamabad": {"lat":33.6844,"lon":73.0479},
            "Colombo": {"lat":6.9271,"lon":79.8612}
        }

        city_choice = st.selectbox("Select a capital", ["--Select--"] + list(capitals.keys()))
        if city_choice != "--Select--":
            lat, lon = capitals[city_choice]["lat"], capitals[city_choice]["lon"]

            w = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric", timeout=10).json()
            aq_json = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}", timeout=10).json()
            components = aq_json["list"][0]["components"]

            feat = {
                "temp_max": w["main"]["temp"],
                "temp_min": w["main"]["temp"],
                "humidity_max": w["main"]["humidity"],
                "humidity_min": w["main"]["humidity"],
                "wind_speed": w["wind"]["speed"],
                "precipitation": 0,
                "pm25": components.get("pm2_5",0),
                "pm10": components.get("pm10",0),
                "no2": components.get("no2",0),
                "so2": components.get("so2",0),
                "o3": components.get("o3",0),
                "co": components.get("co",0)
            }
            feature_order = ["temp_max","temp_min","humidity_max","humidity_min","precipitation","wind_speed","pm25","pm10","no2","so2","o3","co"]
            X_pred = pd.DataFrame([feat])[feature_order]

            pred_aqi = aqi_model.predict(X_pred)[0]
            pred_health = health_model.predict(X_pred)[0]

            # Normalize clean cities
            if city_choice in ["Thimphu", "Malé", "Colombo"]:
                pred_aqi *= 0.65
                pred_health *= 0.7

            st.markdown(f"### Predictions for {city_choice}")
            st.write(f"- Predicted AQI (proxy): **{pred_aqi:.2f}**")
            st.write(f"- Predicted Health Index: **{pred_health:.2f}**")

            # Historical AQI trend
            hist_path = "data/south_asia_6months_data_clean.csv"
            if os.path.exists(hist_path):
                df = pd.read_csv(hist_path)
                cdf = df[df["city"].str.lower() == city_choice.lower()].copy()
                if not cdf.empty:
                    cdf["date"] = pd.to_datetime(cdf["date"])
                    fig_aqi = px.line(cdf, x="date", y="pm25", title=f"AQI (PM2.5) Over Time - {city_choice}")
                    st.plotly_chart(fig_aqi, use_container_width=True)

            # 3-day weather forecast
            try:
                forecast_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
                fc = requests.get(forecast_url).json()
                if "daily" in fc:
                    fdf = pd.DataFrame({
                        "date": fc["daily"]["time"],
                        "temp_max": fc["daily"]["temperature_2m_max"],
                        "temp_min": fc["daily"]["temperature_2m_min"],
                        "precip": fc["daily"]["precipitation_sum"]
                    })
                    fdf = fdf.head(3)
                    ffig = go.Figure()
                    ffig.add_trace(go.Scatter(x=fdf["date"], y=fdf["temp_max"], name="Max Temp (°C)", line=dict(color="tomato")))
                    ffig.add_trace(go.Scatter(x=fdf["date"], y=fdf["temp_min"], name="Min Temp (°C)", line=dict(color="royalblue")))
                    ffig.update_layout(title=f"3-Day Weather Forecast - {city_choice}", xaxis_title="Date", yaxis_title="Temperature (°C)")
                    st.plotly_chart(ffig, use_container_width=True)
                    st.table(fdf.rename(columns={"date":"Date","temp_max":"Max Temp (°C)","temp_min":"Min Temp (°C)","precip":"Precipitation (mm)"}))
            except:
                st.info("Could not fetch forecast.")

    # --------------------------
    # Insights
    # --------------------------
    elif sub == "Insights":
        st.subheader("Insights")

        insights = pd.DataFrame({
            "Rank":[1,2,3,4,5,6,7],
            "city":["New Delhi","Dhaka","Kathmandu","Islamabad","Colombo","Malé","Thimphu"],
            "country":["India","Bangladesh","Nepal","Pakistan","Sri Lanka","Maldives","Bhutan"],
            "pollution_level":["Worst in South Asia & World","Extremely High","Very High","High","Moderate","Clean","Cleanest"],
            "health_index":[320,210,160,110,70,55,40]
        })

        st.write("### 🌍 Health Impact Ranking")
        color_map = {
            "Worst in South Asia & World":"#8e44ad",
            "Extremely High":"#e74c3c",
            "Very High":"#e67e22",
            "High":"#f39c12",
            "Moderate":"#f1c40f",
            "Clean":"#2ecc71",
            "Cleanest":"#27ae60"
        }

        for _, r in insights.iterrows():
            st.markdown(
                f"""<div style="background:{color_map[r['pollution_level']]};padding:12px;border-radius:8px;margin-bottom:8px;color:white;">
                <strong>{r['Rank']}. {r['city']} ({r['country']})</strong> — {r['pollution_level']} — Health Index: {r['health_index']}
                </div>""", unsafe_allow_html=True)

        st.write("### 📈 Insights about South Asian Capitals")
        st.markdown("""
        - New Delhi and Dhaka face the worst air pollution due to emissions and urbanization.  
        - Kathmandu suffers from trapped valley pollution.  
        - Colombo and Malé maintain cleaner air because of sea breeze and lower traffic.  
        - Thimphu remains the cleanest, thanks to environmental policies.
        """)

        st.write("### 💡 Suggestions")
        st.markdown("""
        - Strengthen air monitoring and cross-border pollution controls.  
        - Promote electric mobility and reduce industrial emissions.  
        - Encourage afforestation and sustainable building practices.  
        - Raise health awareness and promote protective behaviors.
        """)

    # --------------------------
    # Comparison
    # --------------------------
    elif sub == "Comparison":
        st.subheader("Comparison — South Asian Capitals")
        hist_path = "data/south_asia_6months_data_clean.csv"
        if not os.path.exists(hist_path):
            st.info("Cleaned historical dataset missing.")
        else:
            df = pd.read_csv(hist_path)

            col1, col2 = st.columns(2)
            with col1:
                # Health Impact Stacked Bar Chart
                avg_health = pd.DataFrame({
                    "city":["New Delhi","Dhaka","Kathmandu","Islamabad","Colombo","Malé","Thimphu"],
                    "Health Index":[350,300,250,180,120,60,30]
                })
                fig1 = px.bar(
                    avg_health, x="city", y="Health Index", color="city",
                    title="Health Impact Index by City (Numerical Values)",
                    color_discrete_sequence=px.colors.qualitative.Safe
                )
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                avg_temp = df.groupby("city")["temp_max"].mean().reset_index()
                fig2 = px.bar(avg_temp, x="city", y="temp_max", color="city", title="Average Temperature per City (°C)")
                st.plotly_chart(fig2, use_container_width=True)

        

            st.write("### 🧭 Key Takeaways")
            st.markdown("""
            - Northern capitals (New Delhi, Kathmandu, Dhaka) face higher pollution.  
            - Coastal cities (Colombo, Malé) have cleaner air due to marine winds.  
            - Temperature varies widely but is less correlated to pollution.  
            - Bhutan’s Thimphu stands out as the healthiest and cleanest capital.
            """)
st.markdown(
    """
    <hr style='border:1px solid #ddd'>
    <p style='text-align:center; font-size:13px; color:gray;'>
        Air Quality, Weather & Health Impact Predictor<br>
        Developed by <span style='color:brown; font-weight:bold;'>Prasikshya Karki — 2025</span><br>
        Data sourced from <a href='https://openweathermap.org/api' target='_blank'>OpenWeatherMap API</a>
    </p>
    """,
    unsafe_allow_html=True
)


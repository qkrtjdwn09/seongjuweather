import streamlit as st
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="Seongju Weather", page_icon="🌤️", layout="centered")

st.title("🌤️ Seongju Weather Explorer")
st.caption("Powered by Open-Meteo API")

# --------------------------
# User input
# --------------------------
city = st.text_input("Enter a city:", "Seoul")

# City coordinates (we’ll map a few common ones)
cities = {
    "Seoul": (37.5665, 126.9780),
    "Busan": (35.1796, 129.0756),
    "Daegu": (35.8714, 128.6014),
    "Jeju": (33.4996, 126.5312)
}

if city not in cities:
    st.warning("City not recognized. Try: Seoul, Busan, Daegu, or Jeju.")
else:
    lat, lon = cities[city]

    # --------------------------
    # Dates
    # --------------------------
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    # --------------------------
    # Fetch data from Open-Meteo
    # --------------------------
    def get_weather_data(base_url, start_date, end_date):
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "daily": "temperature_2m_max,temperature_2m_min",
            "timezone": "auto"
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch data.")
            return None

    # Fetch each
    yesterday_data = get_weather_data("https://archive-api.open-meteo.com/v1/archive", yesterday, yesterday)
    today_data = get_weather_data("https://api.open-meteo.com/v1/forecast", today, today)
    tomorrow_data = get_weather_data("https://api.open-meteo.com/v1/forecast", tomorrow, tomorrow)

    # --------------------------
    # Display
    # --------------------------
    def display_day(label, data):
        if data:
            temp_max = data["daily"]["temperature_2m_max"][0]
            temp_min = data["daily"]["temperature_2m_min"][0]
            st.metric(label=label, value=f"🌡️ High: {temp_max}°C", delta=f"Low: {temp_min}°C")

    st.subheader(f"Weather in {city}")
    col1, col2, col3 = st.columns(3)
    with col1:
        display_day("Yesterday", yesterday_data)
    with col2:
        display_day("Today", today_data)
    with col3:
        display_day("Tomorrow", tomorrow_data)

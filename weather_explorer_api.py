import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta

st.set_page_config(page_title="🇰🇷 Korea Weather Explorer", page_icon="🌦️", layout="wide")

st.title("🇰🇷 Korea Weather Explorer")
st.caption("Interactive temperature map using Open-Meteo API — click anywhere in Korea!")

# --------------------------
# Default Map
# --------------------------
center_lat, center_lon = 36.5, 127.8  # Korea center

m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

# Let user click
st.write("🗺️ Click on any location in Korea to get yesterday, today, and tomorrow’s high/low temperatures.")
map_data = st_folium(m, height=500, width=900)

# --------------------------
# If user clicked on the map
# --------------------------
if map_data and map_data["last_clicked"]:
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    st.success(f"📍 Selected Location: ({lat:.3f}, {lon:.3f})")

    # --------------------------
    # Dates
    # --------------------------
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    # --------------------------
    # Function to get data
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
        r = requests.get(base_url, params=params)
        if r.status_code == 200:
            return r.json()
        else:
            st.error(f"❌ Failed to fetch data from {base_url}")
            return None

    # --------------------------
    # Fetch Data
    # --------------------------
    yesterday_data = get_weather_data("https://archive-api.open-meteo.com/v1/archive", yesterday, yesterday)
    today_data = get_weather_data("https://api.open-meteo.com/v1/forecast", today, today)
    tomorrow_data = get_weather_data("https://api.open-meteo.com/v1/forecast", tomorrow, tomorrow)

    # --------------------------
    # Display Metrics
    # --------------------------
    def display_day(label, data):
        if data and "daily" in data:
            tmax = data["daily"]["temperature_2m_max"][0]
            tmin = data["daily"]["temperature_2m_min"][0]
            st.metric(label, f"High {tmax}°C", f"Low {tmin}°C")
        else:
            st.write(f"{label}: Data not available")

    st.subheader("🌡️ Temperature Overview")

    col1, col2, col3 = st.columns(3)
    with col1:
        display_day("Yesterday", yesterday_data)
    with col2:
        display_day("Today", today_data)
    with col3:
        display_day("Tomorrow", tomorrow_data)
else:
    st.info("Click on the map to fetch weather data.")

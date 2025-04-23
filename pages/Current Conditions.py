import datetime
import streamlit as st
from weather_api import get_weather_data
from soaring_logic import calculate_soaring_score, calculate_thermal_prediction

def format_weather_data(data):
    location = data.get("name", "Unknown Location")
    temperature = data["main"].get("temp", "N/A")
    feels_like = data["main"].get("feels_like", "N/A")
    temp_min = data["main"].get("temp_min", "N/A")
    temp_max = data["main"].get("temp_max", "N/A")
    humidity = data["main"].get("humidity", "N/A")
    weather_desc = data["weather"][0].get("description", "N/A").capitalize()
    wind_speed = data["wind"].get("speed", "N/A")
    wind_deg = data["wind"].get("deg", "N/A")
    clouds = data["clouds"].get("all", "N/A")
    sunrise = data["sys"].get("sunrise", None)
    sunset = data["sys"].get("sunset", None)

    # Convert timestamps to readable time (local or UTC)
    sunrise_time = datetime.datetime.utcfromtimestamp(sunrise).strftime('%I:%M %p UTC') if sunrise else "N/A"
    sunset_time = datetime.datetime.utcfromtimestamp(sunset).strftime('%I:%M %p UTC') if sunset else "N/A"

    # Scoring
    soaring_score = calculate_soaring_score(data)
    thermal_score = calculate_thermal_prediction(data)

    report = f"""
### Weather Report for **{location}**

**Conditions:**
- {weather_desc}
- Temperature: {temperature}°F (Feels like: {feels_like}°F)
- Low: {temp_min}°F, High: {temp_max}°F
- Humidity: {humidity}%
- Wind: {wind_speed} m/s at {wind_deg}°
- Cloud Coverage: {clouds}%

**Sunrise & Sunset:**
- 🌅 Sunrise: {sunrise_time}
- 🌇 Sunset: {sunset_time}

**Soaring Predictions:**
- 🪂 Gliding Score: **{soaring_score}/10**
- 🔥 Thermal Prediction Score: **{thermal_score}/10**
    """

    return report

# Streamlit app
st.title("⛅ GlideWx: Current Conditions")

location = st.text_input("Enter your glider location (e.g., Memphis):")

if location:
    data = get_weather_data(location)

    if data:
        st.markdown(format_weather_data(data))
    else:
        st.error("Unable to retrieve weather data. Please check the location or try again later.")

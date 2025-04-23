import datetime
import streamlit as st
from weather_api import get_coordinates, get_forecast
from soaring_logic import calculate_soaring_score_forecast, calculate_thermal_prediction_forecast

st.title("📆 7-Day Glider Soaring Forecast")

location = st.text_input("Enter the location to forecast (e.g., Memphis):")

if location:
    lat, lon = get_coordinates(location)

    if lat is None or lon is None:
        st.error("Could not find coordinates for that location.")
    else:
        forecast_data = get_forecast(lat, lon)

        if forecast_data and "daily" in forecast_data:
            st.subheader(f"🌍 7-Day Forecast for **{location}**")

            for day in forecast_data["daily"]:
                st.markdown("---")
                date = datetime.datetime.utcfromtimestamp(day["dt"]).strftime('%A, %B %d, %Y')
                temp = day["temp"]["day"]
                wind = day["wind_speed"]
                rain = day.get("pop", 0) * 100  # Probability of precipitation
                clouds = day["clouds"]
                desc = day["weather"][0]["description"].capitalize()

                soaring_score = calculate_soaring_score_forecast(day)
                thermal_score = calculate_thermal_prediction_forecast(day)

                st.markdown(f"""
### 📅 {date}
**🌤️ Description:** {desc}  
**🌡️ Temperature:** {temp}°F  
**💨 Wind Speed:** {wind} m/s  
**🌧️ Rain Chance:** {rain:.0f}%  
**☁️ Cloud Coverage:** {clouds}%  

**🪂 Soaring Score:** **{soaring_score}/10**  
**🔥 Thermal Prediction:** **{thermal_score}/10**
                """)

        else:
            st.error("Could not retrieve forecast data. Please try again later.")

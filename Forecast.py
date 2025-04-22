import datetime
import streamlit as st
from weather_api import get_coordinates, get_forecast
from soaring_logic import calculate_soaring_score_forecast, calculate_thermal_prediction_forecast

st.title("Forecast - Multi-Day Glider Weather")

location = st.text_input("Enter the location to forecast (e.g., Memphis):")
if location:
    lat, lon = get_coordinates(location)
    if lat is None or lon is None:
        st.write("Could not find coordinates for that location.")
    else:
        forecast_data = get_forecast(lat, lon)

        if forecast_data and "daily" in forecast_data:
            st.subheader(f"7-Day Forecast for {location}")

            for day in forecast_data["daily"]:
                    st.markdown("---")
                    date = datetime.datetime.utcfromtimestamp(day["dt"]).strftime('%A, %B %d, %Y')
                    temp = day["temp"]["day"]
                    wind = day["wind_speed"]
                    rain = day.get("pop", 0) * 100  # Probability of precipitation
                    clouds = day["clouds"]
                    desc = day["weather"][0]["description"]

                    st.text(f"Date: {date}")
                    st.text(f"Description: {desc.capitalize()}")
                    st.text(f"Temperature: {temp}°F")
                    st.text(f"Wind Speed: {wind} m/s")
                    st.text(f"Rain Chance: {rain:.0f}%")
                    st.text(f"Cloud Coverage: {clouds}%")
                    st.text(f"Soaring Score: {calculate_soaring_score_forecast(day)}/10")
                    st.text(f"Thermal Prediction Score: {calculate_thermal_prediction_forecast(day)}/10")

        else:
            st.write("Could not get forecast data.")

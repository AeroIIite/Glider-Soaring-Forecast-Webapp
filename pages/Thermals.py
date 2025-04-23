import datetime
import streamlit as st
import folium
from weather_api import get_coordinates, get_forecast
from soaring_logic import calculate_thermal_prediction_forecast, calculate_soaring_score_forecast
from streamlit.components.v1 import html

def calculate_thermal_intensity(temp, wind_speed, cloud_cover):
    return (temp > 75) + (wind_speed < 5) + (20 <= cloud_cover <= 50)

def best_thermal_hours(hourly_data):
    best_hours = []
    for hour in hourly_data:
        if hour["temp"] > 75 and hour["wind_speed"] < 5 and 20 <= hour["clouds"] <= 50:
            best_hours.append(hour["dt"])
    return best_hours

def display_thermal_map(lat, lon, forecast_data):
    m = folium.Map(location=[lat, lon], zoom_start=10)
    nearby_locs = [(lat + 0.01, lon + 0.01), (lat + 0.02, lon + 0.02)]

    for loc in nearby_locs:
        t_intensity = calculate_thermal_intensity(
            forecast_data["daily"][0]["temp"]["day"],
            forecast_data["daily"][0]["wind_speed"],
            forecast_data["daily"][0]["clouds"]
        )
        folium.CircleMarker(
            location=loc,
            radius=10,
            color='green' if t_intensity > 1 else 'red',
            fill=True,
            fill_color='green' if t_intensity > 1 else 'red',
            fill_opacity=0.6,
            popup=f"Thermal Intensity: {t_intensity}/3"
        ).add_to(m)

    html(m._repr_html_(), height=500)

def thermals_page():
    st.title("🔥 GlideWX: Thermal Glider Forecast")

    st.markdown("### 📍 Enter a Location to Begin")
    location = st.text_input("Enter your location (e.g., Memphis):")

    if location:
        lat, lon = get_coordinates(location)

        if lat is None or lon is None:
            st.error("❌ Could not find coordinates for that location.")
            return

        forecast_data = get_forecast(lat, lon)
        if not forecast_data:
            st.error("⚠️ Could not retrieve forecast data.")
            return

        st.markdown("---")
        st.subheader(f"🗺️ Thermal Intensity Map for **{location}**")
        display_thermal_map(lat, lon, forecast_data)

        st.markdown("---")
        if "hourly" in forecast_data:
            best_hours = best_thermal_hours(forecast_data["hourly"])
            if best_hours:
                best_hours_str = [datetime.datetime.utcfromtimestamp(h).strftime('%I:%M %p') for h in best_hours]
                st.success("🌤️ Best hours for thermaling today:")
                st.write(", ".join(best_hours_str))
            else:
                st.warning("No optimal thermal hours found for today.")
        else:
            st.warning("Hourly forecast data not available.")

        st.markdown("---")
        st.subheader(f"📅 Detailed 7-Day Forecast for {location}")
        for day in forecast_data.get("daily", []):
            with st.expander(datetime.datetime.utcfromtimestamp(day["dt"]).strftime('%A, %B %d, %Y')):
                st.markdown(f"**Weather**: {day['weather'][0]['description'].capitalize()}")
                st.markdown(f"- 🌡️ Temp: {day['temp']['day']}°F")
                st.markdown(f"- 💨 Wind: {day['wind_speed']} m/s")
                st.markdown(f"- 🌧️ Rain Chance: {day.get('pop', 0) * 100:.0f}%")
                st.markdown(f"- ☁️ Cloud Cover: {day['clouds']}%")
                st.markdown(f"- 🪂 Soaring Score: **{calculate_soaring_score_forecast(day)}/10**")
                st.markdown(f"- 🔥 Thermal Prediction: **{calculate_thermal_prediction_forecast(day)}/10**")

        st.markdown("---")
        with st.expander("ℹ️ How are thermals predicted?"):
            st.markdown("""
            - **Temperature**: Above 75°F improves thermal chances.
            - **Wind Speed**: Below 5 m/s is ideal.
            - **Clouds**: Partial clouds (20–50%) are favorable.
            - **Pressure**: Lower pressure helps form thermals.
            """)

# Run page
if __name__ == "__main__":
    thermals_page()

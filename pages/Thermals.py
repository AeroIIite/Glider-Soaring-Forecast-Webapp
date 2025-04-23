import datetime
import streamlit as st
import folium
from weather_api import get_coordinates, get_forecast
from soaring_logic import calculate_thermal_prediction, calculate_soaring_score_forecast, calculate_thermal_prediction_forecast

def calculate_thermal_intensity(temp, wind_speed, cloud_cover):
    """Calculate thermal intensity based on temperature, wind speed, and cloud cover."""
    temp_score = temp > 75  # Only temperatures above 75°F are considered for thermals
    wind_score = wind_speed < 5  # Light winds are better for thermals
    cloud_score = 20 <= cloud_cover <= 50  # Partial clouds are favorable for thermals
    return temp_score + wind_score + cloud_score

def best_thermal_hours(hourly_data):
    """Identify the best thermal hours based on forecast conditions."""
    best_hours = []
    for hour in hourly_data:
        temp = hour["temp"]
        wind_speed = hour["wind_speed"]
        cloud_cover = hour["clouds"]
        if temp > 75 and wind_speed < 5 and 20 <= cloud_cover <= 50:
            best_hours.append(hour["dt"])  # Add the timestamp of the best hours
    return best_hours

def display_thermal_map(lat, lon, forecast_data):
    """Display thermal intensity on a map using Folium."""
    m = folium.Map(location=[lat, lon], zoom_start=10)
    locations = [(lat + 0.01, lon + 0.01), (lat + 0.02, lon + 0.02)]  # Nearby points for simplicity
    thermal_intensity_scores = []

    # Calculate thermal intensity for each location
    for loc in locations:
        lat, lon = loc
        temp = forecast_data["daily"][0]["temp"]["day"]  # Day temperature
        wind_speed = forecast_data["daily"][0]["wind_speed"]
        cloud_cover = forecast_data["daily"][0]["clouds"]
        thermal_intensity_scores.append(calculate_thermal_intensity(temp, wind_speed, cloud_cover))

    # Add markers to the map based on thermal intensity
    for i, loc in enumerate(locations):
        folium.CircleMarker(
            location=loc,
            radius=10,
            color='green' if thermal_intensity_scores[i] > 1 else 'red',
            fill=True,
            fill_color='green' if thermal_intensity_scores[i] > 1 else 'red',
            fill_opacity=0.6,
            popup=f"Thermal Intensity: {thermal_intensity_scores[i]}"
        ).add_to(m)

    # Render the map in Streamlit
    st.components.v1.html(m._repr_html_(), width=700, height=500)

def thermals_page():
    st.title("Thermal Glider Forecast - Thermals")

    # Get location input
    location = st.text_input("Enter your location (e.g., Memphis):")

    if location:
        # Get coordinates for the location
        lat, lon = get_coordinates(location)

        if lat is None or lon is None:
            st.write("Could not find coordinates for that location.")
        else:
            # Get forecast data for the location
            forecast_data = get_forecast(lat, lon)

            if forecast_data:
                if "daily" in forecast_data:
                    # Thermal Intensity Map
                    st.subheader(f"Thermal Intensity Map for {location}")
                    display_thermal_map(lat, lon, forecast_data)

                    # Best Thermal Hours - Error handling for missing 'hourly' key
                    if "hourly" in forecast_data:
                        best_hours = best_thermal_hours(forecast_data["hourly"])
                        best_hours_str = [datetime.datetime.utcfromtimestamp(hour).strftime('%H:%M') for hour in best_hours]

                        st.subheader("Best Thermal Hours")
                        if best_hours_str:
                            st.write("The best hours for thermal gliding are:")
                            st.write(", ".join(best_hours_str))
                        else:
                            st.write("No optimal thermal hours found for today.")
                    else:
                        st.write("Hourly forecast data is not available.")

                    # Additional weather details and scores
                    st.subheader(f"Weather Forecast for {location}")

                    for day in forecast_data["daily"]:
                        date = datetime.datetime.utcfromtimestamp(day["dt"]).strftime('%A, %B %d, %Y')
                        temp = day["temp"]["day"]
                        wind = day["wind_speed"]
                        rain = day.get("pop", 0) * 100  # Probability of precipitation
                        clouds = day["clouds"]
                        desc = day["weather"][0]["description"]

                        st.markdown(f"---\n**Date**: {date}")
                        st.text(f"Description: {desc.capitalize()}")
                        st.text(f"Temperature: {temp}°F")
                        st.text(f"Wind Speed: {wind} m/s")
                        st.text(f"Rain Chance: {rain:.0f}%")
                        st.text(f"Cloud Coverage: {clouds}%")
                        st.text(f"Soaring Score: {calculate_soaring_score_forecast(day)}/10")
                        st.text(f"Thermal Prediction Score: {calculate_thermal_prediction_forecast(day)}/10")

                else:
                    st.write("Could not retrieve daily forecast data.")

            else:
                st.write("Could not retrieve forecast data.")

    st.markdown("""
    How thermals are predicted:

    - **Temperature**: A temperature above 75°F increases the chance of thermals.
    - **Wind Speed**: Winds below 5 m/s are favorable for thermals because stronger winds may disrupt thermal formation.
    - **Cloud Coverage**: Partial cloud cover (20-50%) often indicates that thermals are forming, especially with cumulus clouds.
    - **Pressure**: Lower pressure systems often enhance thermal formation.
    """)

# Running the page
if __name__ == "__main__":
    thermals_page()

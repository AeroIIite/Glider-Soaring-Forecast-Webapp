import datetime
import streamlit as st
from weather_api import get_weather_data
from soaring_logic import calculate_soaring_score, calculate_thermal_prediction

def format_weather_data(data):
    # Extract relevant details
    location = data.get("name", "Unknown Location")
    temperature = data["main"].get("temp", "N/A")
    feels_like = data["main"].get("feels_like", "N/A")
    temp_min = data["main"].get("temp_min", "N/A")
    temp_max = data["main"].get("temp_max", "N/A")
    humidity = data["main"].get("humidity", "N/A")
    weather_desc = data["weather"][0].get("description", "N/A")
    wind_speed = data["wind"].get("speed", "N/A")
    wind_deg = data["wind"].get("deg", "N/A")
    clouds = data["clouds"].get("all", "N/A")
    sunrise = data["sys"].get("sunrise", "N/A")
    sunset = data["sys"].get("sunset", "N/A")

    # Convert timestamp to readable time
    if sunrise != "N/A":
        sunrise_time = datetime.datetime.utcfromtimestamp(sunrise).strftime('%Y-%m-%d %H:%M:%S')
    if sunset != "N/A":
        sunset_time = datetime.datetime.utcfromtimestamp(sunset).strftime('%Y-%m-%d %H:%M:%S')

    # Calculate soaring score
    soaring_score = calculate_soaring_score(data)

    # Formatting output with extra spacing for readability
    output = f"Weather Report for {location}:\n\n"
    output += f"Description: {weather_desc.capitalize()}\n\n"
    output += f"Temperature: {temperature}°F (Feels like: {feels_like}°F)\n"
    output += f"Min Temperature: {temp_min}°F, Max Temperature: {temp_max}°F\n\n"
    output += f"Humidity: {humidity}%\n\n"
    output += f"Wind Speed: {wind_speed} m/s at {wind_deg}°\n\n"
    output += f"Cloud Coverage: {clouds}%\n\n"
    output += f"Sunrise: {sunrise_time}\n"
    output += f"Sunset: {sunset_time}\n\n"
    output += f"Gliding Score: {soaring_score}/10\n\n"
    output += f"Thermal Prediction Score: {calculate_thermal_prediction(data)}/10"

    return output

st.title("Glider Soaring Weather Predictor")

location = st.text_input("Enter your glider location (e.g., Memphis):")
    # ... rest of your code
# Assuming the function `get_weather_data` properly fetches data
data = get_weather_data(location)

# Call the function and display the formatted weather data
if data:
    formatted_weather = format_weather_data(data)
    st.text(formatted_weather)  # Use `st.text()` to ensure proper line breaks
else:
    st.write("Unable to retrieve weather data. Please try again.")

st.text("""
How these thermals are predicted:

Temperature: A temperature above 75°F increases the chance of thermals.

Wind Speed: Winds below 5 m/s are favorable for thermals because stronger winds may disrupt the development of thermals.

Clouds: Partial cloud cover (around 20-50%) often indicates that thermals are forming, especially with cumulus clouds.

Pressure: Lower pressure systems often enhance thermal formation.
        """)

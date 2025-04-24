import datetime
import requests
import streamlit as st
from weather_api import get_coordinates, get_forecast
from soaring_logic import calculate_soaring_score_forecast, calculate_thermal_prediction_forecast

# Function to calculate weather impact based on wind speed and temperature
def calculate_weather_impact(glider, day_weather):
    wind_speed = day_weather['wind_speed']
    temperature = day_weather['temp']['day']
    clouds = day_weather['clouds']

    # Glider-specific factors
    optimal_wind_range = glider['optimal_wind_range']

    # Weather impact logic
    wind_impact = "Good" if optimal_wind_range[0] <= wind_speed <= optimal_wind_range[1] else "Poor"
    thermal_impact = "Good" if temperature > 75 and clouds <= 50 else "Poor"

    # Combine impacts
    performance = "Optimal" if wind_impact == "Good" and thermal_impact == "Good" else "Suboptimal"

    return {
        "wind_impact": wind_impact,
        "thermal_impact": thermal_impact,
        "performance": performance
    }

# Function to compare glider performance with forecast data
def compare_with_forecast():
    st.title("Compare Your Glider with 7-Day Weather Forecast")

    # Input for Glider Type
    glider_name = st.text_input("Enter Your Glider's Name/Model:")
    with st.expander("ℹ️ What Do 'Minimum' and 'Maximum Optimal Wind Speed' Mean?"):
        st.markdown("""
        ### 💨 Wind Speed Range for Soaring Performance

        Your glider performs best within a certain **range of wind speeds**. Here's what each input means:

        - **Minimum Optimal Wind Speed (m/s):**
          The lowest wind speed at which your glider starts performing well. Below this, there may not be enough lift, especially from thermals or ridge lift.

        - **Maximum Optimal Wind Speed (m/s):**
          The highest wind speed where your glider still performs well. Above this, conditions might become turbulent or thermals may be disrupted.

        ### ✈️ Example
        For a glider like the *Discus-2*, a good range might be:
        - **Min:** `2 m/s` (Thermals become usable)
        - **Max:** `6 m/s` (Smooth soaring without too much turbulence)

        This range helps us compare your glider with the forecast and tell you how well it might perform in upcoming weather conditions.
        """)

    # Input for Glider Specifications
    optimal_wind_min = st.number_input("Enter Minimum Optimal Wind Speed (m/s):", min_value=0, step=1)
    optimal_wind_max = st.number_input("Enter Maximum Optimal Wind Speed (m/s):", min_value=0, step=1)
    glide_ratio = st.number_input("Enter Your Glider's Glide Ratio (e.g., 40 for 40:1):", min_value=0)

    # Input for Weather City and API Key
    location = st.text_input("Enter the City for Weather Forecast:")
    api_key = st.secrets["weather_api_key"]

    # When all inputs are provided
    if glider_name and location and api_key:
        glider_info = {
            "name": glider_name,
            "optimal_wind_range": (optimal_wind_min, optimal_wind_max),
            "glide_ratio": glide_ratio
        }

        # Get coordinates for location
        lat, lon = get_coordinates(location)

        if lat is None or lon is None:
            st.error("Could not find coordinates for that location.")
        else:
            forecast_data = get_forecast(lat, lon)

            if forecast_data and "daily" in forecast_data:
                st.subheader(f"🌍 7-Day Forecast for **{location}**")

                # Loop through the daily forecast data and display comparison
                for day in forecast_data["daily"]:
                    date = datetime.datetime.utcfromtimestamp(day["dt"]).strftime('%A, %B %d, %Y')
                    wind_speed = day["wind_speed"]
                    temperature = day["temp"]["day"]
                    clouds = day["clouds"]
                    desc = day["weather"][0]["description"].capitalize()

                    # Compare the weather impact on the glider
                    weather_impact = calculate_weather_impact(glider_info, day)

                    st.markdown(f"""
### 📅 {date}
**🌤️ Description:** {desc}  
**🌡️ Temperature:** {temperature}°F  
**💨 Wind Speed:** {wind_speed} m/s  
**☁️ Cloud Coverage:** {clouds}%  

**🪂 Wind Impact:** {weather_impact['wind_impact']}  
**🔥 Thermal Impact:** {weather_impact['thermal_impact']}  
**⚡ Performance:** {weather_impact['performance']}
                    """)

            else:
                st.error("Could not retrieve forecast data. Please try again later.")
    else:
        st.write("Please enter all details to compare.")

# Run the comparison function
compare_with_forecast()

# Sample glider database (you can expand this or load from a file)
glider_data = {
    "ASK-21": {
        "Glide Ratio": "34:1",
        "Stall Speed": "34 knots",
        "Max L/D Speed": "52 knots",
        "Min Sink Rate": "2.1 ft/s",
        "Image URL": "https://upload.wikimedia.org/wikipedia/commons/d/db/Schleicher_ASK_21_%28D-0721%29_02.jpg"
    },
    "DG-1000": {
        "Glide Ratio": "45:1",
        "Stall Speed": "38 knots",
        "Max L/D Speed": "60 knots",
        "Min Sink Rate": "1.7 ft/s",
        "Image URL": "https://upload.wikimedia.org/wikipedia/commons/7/79/DG1000_glider_crop.jpg"
    },
    "ASW-27": {
        "Glide Ratio": "48:1",
        "Stall Speed": "40 knots",
        "Max L/D Speed": "65 knots",
        "Min Sink Rate": "1.5 ft/s",
        "Image URL": "https://upload.wikimedia.org/wikipedia/commons/8/80/Schleicher_ASW27b.jpg"
    },
    "PW-5": {
        "Glide Ratio": "32:1",
        "Stall Speed": "36 knots",
        "Max L/D Speed": "43 knots",
        "Min Sink Rate": "2.8 ft/s",
        "Image URL": "https://upload.wikimedia.org/wikipedia/commons/b/bb/Szybowiec_PW-5_w_locie.jpg"
    },
    "SGS 1-26": {
        "Glide Ratio": "23:1",
        "Stall Speed": "31 knots",
        "Max L/D Speed": "43 knots",
        "Min Sink Rate": "2.9 ft/s",
        "Image URL": "https://upload.wikimedia.org/wikipedia/commons/0/09/C-FPPMairborne.jpg"
    },
    "L-33": {
        "Glide Ratio": "33:1",
        "Stall Speed": "35 knots",
        "Max L/D Speed": "45 knots",
        "Min Sink Rate": "2.25 ft/s",
        "Image URL": "https://upload.wikimedia.org/wikipedia/commons/1/12/LET_L-33_Solo_glider_at_Air_Sailing_Gliderport.jpg"
    },
    "Blanik L-23": {
        "Glide Ratio": "28:1",
        "Stall Speed": "32 knots",
        "Max L/D Speed": "49 knots",
        "Min Sink Rate": "2.6 ft/s",
        "Image URL": "https://live.staticflickr.com/65535/53468330865_8f2d8dfac7_o.jpg"
    }
}

st.title("🛩️ Glider Specifications")

selected_glider = st.selectbox("Select Your Glider:", list(glider_data.keys()))

if selected_glider:
    info = glider_data[selected_glider]
    st.subheader(f"Specs for {selected_glider}")
    st.image(info["Image URL"], width=400)
    for key, value in info.items():
        if key != "Image URL":
            st.markdown(f"**{key}:** {value}")

# Optional: Custom glider entry
st.markdown("---")
st.subheader("Can't find your Glider?")
st.markdown("👉 [Submit Your Glider Info](https://docs.google.com/forms/d/e/1FAIpQLScSY6Ww668qT2z5tEtjVoQD9ItB4lIrRF-gMmybOVRG6qO4MQ/viewform?usp=dialog)")

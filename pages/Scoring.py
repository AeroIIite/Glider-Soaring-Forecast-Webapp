import streamlit as st

st.markdown("---")
st.header("🧮 How the Soaring Scores Work")

st.markdown("#### 🪂 Soaring Score")
st.markdown("""
A quick 1–10 snapshot of daily gliding potential based on:
- 🌬️ Wind Speed
- ☁️ Cloud Coverage
- 🌡️ Temperature
- 🌧️ Precipitation Chance
""")

st.markdown("#### 🌡️ Thermal Prediction Score")
st.markdown("""
Estimates thermal generation likelihood using:
- 🌡️ Temperature (75°F+)
- 💨 Light Winds (< 5 m/s)
- ☁️ Cumulus Clouds (20–50% cover)
- 🔽 Low Pressure Systems
""")

st.info("These tools help recreational glider pilots, but always use your judgment and local weather data before flying.")

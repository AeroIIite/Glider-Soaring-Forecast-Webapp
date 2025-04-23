import streamlit as st

st.set_page_config(page_title="GlideWX", page_icon="🛩️", layout="centered")

# Header
st.title("🛩️ GlideWX")
st.subheader("Your Soaring Companion for Thermal Forecasting")

st.markdown("""
Welcome to **GlideWX**, your intelligent gliding weather assistant.

Whether you're planning a local thermal flight or chasing conditions across multiple days, GlideWX uses real-time weather data to help you:
- 📍 Forecast thermal soaring potential
- 📊 Score days with gliding conditions
- 🗺️ Visualize thermal intensity and cloud cover
- ⏰ Find the best flying hours

---

### 🧭 Explore the App

Use the navigation sidebar to:
- 🔍 View **Today's Weather**
- 📆 Get a **7-Day Forecast**
- 📈 See **Thermal Predictions**
- 📚 Learn about **How Scoring Works**

---

### 🔧 Built with OpenWeather API + Soaring Science

Enjoy the skies, and happy soaring!
""")


st.title("🧮 How the Soaring Scores Work")

st.markdown("""
This section explains how we calculate the **Soaring Score** and **Thermal Prediction Score** for glider pilots.

---

### 🪂 Soaring Score
The **Soaring Score** is a rating from 1 to 10 based on the overall favorability of the current or forecasted weather conditions for gliding. We take into account:

- **Wind Speed:** Moderate winds are best. Too high can be dangerous or reduce soaring potential.
- **Cloud Coverage:** Partial clouds (20–50%) suggest thermal activity.
- **Temperature:** Warmer temperatures promote thermals.
- **Precipitation Chance:** Lower is better for flying conditions.

The score is designed to give a quick snapshot of how good the conditions are for a fun and safe glide.

---

### 🌡️ Thermal Prediction Score
The **Thermal Prediction Score** measures the likelihood and strength of thermals, which are crucial for unpowered flight:

- **🌡️ Temperature:** Above 75°F is better for thermal generation.
- **💨 Wind Speed:** Below 5 m/s is ideal — higher wind can break up thermals.
- **☁️ Clouds:** 20–50% cloud cover (especially cumulus) signals active thermals.
- **🔽 Pressure:** Lower pressure systems enhance lift.

---

These scores are based on simplified algorithms designed for recreational glider pilots. Always check local weather conditions and use personal judgment before flying.

Fly smart and stay safe! 🛩️
""")

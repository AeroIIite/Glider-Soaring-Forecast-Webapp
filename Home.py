import streamlit as st

st.set_page_config(page_title="GlideWX", page_icon="🛩️", layout="centered")

# ─────────────────────────────────────────────────────
# HEADER
st.title("🛩️ GlideWX")
st.subheader("Smart Thermal Forecasting for Glider Pilots")

st.markdown("---")

# ─────────────────────────────────────────────────────
# APP INTRO
st.markdown("""
GlideWX is your **real-time soaring companion** designed for recreational glider pilots.

It combines live weather data with soaring science to help you make better flying decisions, faster.

### Why Pilots Love GlideWX:
- 📍 **Pinpoint Thermals** – Find areas with strong thermal activity
- 📊 **Daily Soaring Scores** – Get quick-read ratings from 1–10
- ⏰ **Optimal Flight Windows** – Identify the best times to fly
- 🧠 **Simple, Science-Backed Tools** – Built with real soaring logic
""")

st.markdown("---")

# ─────────────────────────────────────────────────────
# FEATURES NAV
st.markdown("### 🚀 Explore the Features")
st.markdown("""
Use the sidebar to access:
- 🔍 **Today’s Weather** — Current soaring forecast
- 📆 **7-Day Outlook** — Multi-day planning for cross-country
- 📈 **Thermal Predictions** — Understand where and when lift forms
- 🧮 **Soaring Score Logic** — Learn how scores are calculated
""")

st.markdown("---")

# ─────────────────────────────────────────────────────
# FEEDBACK SECTION
st.markdown("### 💬 Got Feedback or Suggestions?")
st.markdown("""
We’d love your input to make GlideWX even better.

👉 [Submit Feedback](https://docs.google.com/forms/d/e/1FAIpQLScmohT-qBuh_UPpYZobYElCFVI2XHYYuLTxxBsDhf3VkQvq_A/viewform?usp=dialog)
""")

# Optional touch
st.caption("Built for glider pilots. Powered by OpenWeather + passion for flight.")

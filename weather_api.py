import requests
import streamlit as st

if "weather_api_key" not in st.secrets:
    st.error("API key not found! Did you set it in Streamlit Cloud > Edit secrets?")
else:
    st.success("API key found. Proceeding with request...")


def get_weather_data(city_name):
    api_key = st.secrets["weather_api_key"]
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=imperial"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching weather data: {response.status_code}")
        st.text(response.text)  # Debug output
        return None


def get_coordinates(city_name):
    api_key = st.secrets["weather_api_key"]
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        return lat, lon
    else:
        st.error(f"Error fetching coordinates: {response.status_code}")
        st.text(response.text)
        return None, None


def get_forecast(lat, lon):
    api_key = st.secrets["weather_api_key"]
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&units=imperial&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching forecast data: {response.status_code}")
        st.text(response.text)
        return None

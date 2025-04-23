import requests
import streamlit as st


def get_weather_data(city_name):
    api_key = st.secrets["weather_api_key"]
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=imperial"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        print(f"Error fetching weather data: {response.status_code}")
        return None


def get_coordinates(city_name):
    api_key = st.secrets["weather_api_key"]
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        lat = data['coord']['lat']  # Latitude
        lon = data['coord']['lon']  # Longitude
        print(f"Latitude: {lat}, Longitude: {lon}")
        return lat, lon
    else:
        print(f"Error fetching data: {response.status_code}")
        return None, None


def get_forecast(lat, lon):
    api_key = st.secrets["weather_api_key"]
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&units=imperial&appid={api_key}"
    response = requests.get(url)
    return response.json()

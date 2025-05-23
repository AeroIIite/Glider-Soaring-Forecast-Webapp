import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.weatherapi.com/v1/forecast.json"


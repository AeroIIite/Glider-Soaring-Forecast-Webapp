def calculate_soaring_score(weather_data):
    # Extract relevant weather information
    temp = weather_data["main"].get("temp", None)
    wind_speed = weather_data["wind"].get("speed", None)
    rain_chance = weather_data["weather"][0].get("description", "")

    # Initialize score
    score = 10

    # Adjust score based on temperature
    if temp is not None:
        if temp < 59:  # If the temperature is below 15°C
            score -= 2

    # Adjust score based on wind speed
    if wind_speed is not None:
        if wind_speed > 15:  # If wind speed is more than 25 kph
            score -= 3

    # Adjust score based on chance of rain
    if "rain" in rain_chance.lower():  # If the description includes "rain"
        score -= 3

    # Return a non-negative score
    return max(0, score)

def calculate_thermal_prediction(weather_data):
    # Extract relevant weather data
    temperature = weather_data["main"].get("temp", None)
    wind_speed = weather_data["wind"].get("speed", None)
    clouds = weather_data["clouds"].get("all", None)
    pressure = weather_data["main"].get("pressure", None)

    # Initialize thermal score
    thermal_score = 0

    # Basic conditions for thermals:
    if temperature is not None:
        if temperature > 75:  # Warmer temperature promotes thermals
            thermal_score += 3  # Increase score for warm conditions

    if wind_speed is not None:
        if wind_speed < 5:  # Light wind is ideal for thermals
            thermal_score += 2

    if clouds is not None:
        if 20 < clouds < 50:  # Partial cloud coverage with some cumulus clouds
            thermal_score += 2

    if pressure is not None:
        if pressure < 1015:  # Low pressure is favorable for thermals
            thermal_score += 2

    # Return thermal score (scaled 0–10)
    return min(10, thermal_score)  # Cap at 10


def calculate_soaring_score_forecast(day_data):
    temp = day_data["temp"]["day"]
    wind = day_data["wind_speed"]
    rain = day_data.get("pop", 0) * 100  # Convert to percent

    score = 10

    if temp < 15:
        score -= 2
    if wind > 25:
        score -= 3
    if rain > 20:
        score -= 3

    return max(0, score)


def calculate_thermal_prediction_forecast(day_data):
    temp = day_data["temp"]["day"]
    wind = day_data["wind_speed"]
    clouds = day_data["clouds"]
    pressure = day_data.get("pressure", 1013)  # Default to standard pressure if missing

    score = 5

    if temp > 75:
        score += 2
    if wind < 5:
        score += 1
    if 20 <= clouds <= 50:
        score += 1
    if pressure < 1010:
        score += 1

    return min(10, score)

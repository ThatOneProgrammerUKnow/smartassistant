import os
import requests
from dotenv import load_dotenv

# Initialize
load_dotenv()
weathermaps_api_key = os.getenv("WEATHER_API_KEY")


def get_weather_today():
    """Fetch weather data and return a formatted string."""
    lat = "-33.8622899"
    lon = "18.6588768"
    openweathermaps_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weathermaps_api_key}&units=metric"
    response = requests.get(openweathermaps_url)
    
    if response.status_code == 200:
        data = response.json()
        weather_str = (
            f"Today, the skies are {data['weather'][0]['main']}.\n"
            f"The temperature is now {data['main']['temp']} degrees celsius.\n"
            f"The maximum temperature will be {data['main']['temp_max']} and the minimum temperature will be {data['main']['temp_min']}.\n"
        )
        return weather_str
    else:
        return "Unable to fetch weather data."

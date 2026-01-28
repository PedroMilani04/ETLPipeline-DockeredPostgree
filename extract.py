# extract.py
import requests
from config import BASE_URL

def extract_weather_data(city_info):
    """Extracts data for a specific city"""
    params = {
        "latitude": city_info['lat'],
        "longitude": city_info['lon'],
        "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "timezone": "auto" # 'auto' adjusts timezone to the city location
    }
    
    print(f"1. [EXTRACT] Downloading data for {city_info['name']}...")
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    print(f"❌ Error extracting {city_info['name']}: {response.status_code}")
    return None

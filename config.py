# config.py
# --- 1. CONFIGURATION & DICTIONARY ---
BASE_URL = "https://api.open-meteo.com/v1/forecast"

# Our city "Catalog"
CITIES = {
    "1": {"name": "Sao Paulo", "lat": -23.55, "lon": -46.63},
    "2": {"name": "Rio de Janeiro", "lat": -22.90, "lon": -43.17},
    "3": {"name": "Brasilia", "lat": -15.78, "lon": -47.92},
    "4": {"name": "Salvador", "lat": -12.97, "lon": -38.50},
    "5": {"name": "London (UK)", "lat": 51.50, "lon": -0.12},
    "6": {"name": "Tokyo (JP)", "lat": 35.68, "lon": 139.69}
}

DB_CONNECTION_URI = "postgresql+psycopg2://admin:admin@localhost:5432/weather_db"
import requests
import pandas as pd
from sqlalchemy import create_engine

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

def get_user_selection():
    """Displays the menu and returns the list of chosen cities"""
    print("\n=== CITY MENU ===")
    for key, info in CITIES.items():
        print(f"[{key}] {info['name']}")
    print("[0] All cities")
    
    choice = input("\nEnter city codes (comma separated) or 0 for all: ")
    
    selected_cities = []
    
    if choice.strip() == '0':
        return list(CITIES.values()) # Return all
    
    codes = choice.split(',')
    for code in codes:
        code = code.strip()
        if code in CITIES:
            selected_cities.append(CITIES[code])
        else:
            print(f"⚠️ Invalid code '{code}' ignored.")
            
    return selected_cities

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

def transform_data(raw_data, city_name):
    """Clean up and add city column"""
    hourly = raw_data['hourly']
    df = pd.DataFrame(hourly)
    
    # Conversions
    df['time'] = pd.to_datetime(df['time'])
    
    # Renaming
    column_map = {
        'time': 'timestamp',
        'temperature_2m': 'temperature_celsius',
        'relative_humidity_2m': 'relative_humidity',
        'precipitation': 'precipitation_mm',
        'wind_speed_10m': 'wind_speed_kmh'
    }
    df = df.rename(columns=column_map)
    
    # --- THE MAGIC HERE ---
    # We add a fixed column with the city name
    df['city'] = city_name
    
    return df

def load_data_to_postgres(df):
    """Saves the accumulated DataFrame to PostgreSQL"""
    print(f"3. [LOAD] Saving {len(df)} total lines to Database...")
    try:
        engine = create_engine(DB_CONNECTION_URI)
        # if_exists='replace' will recreate the table with the new data from this execution
        df.to_sql('weather_forecast', engine, if_exists='replace', index=False)
        print("✅ Load complete successfully!")
    except Exception as e:
        print(f"❌ Error saving to database: {e}")

if __name__ == "__main__":
    selected_cities_list = get_user_selection()
    
    if not selected_cities_list:
        print("No city selected. Exiting.")
        exit()
    
    all_dataframes = []
    
    # Main loop: Iterates over each selected city
    for city in selected_cities_list:
        raw_json = extract_weather_data(city)
        if raw_json:
            df_city = transform_data(raw_json, city['name'])
            all_dataframes.append(df_city)
            
    # Consolidation (Merges all tables into one)
    if all_dataframes:
        final_df = pd.concat(all_dataframes, ignore_index=True)
        print("\n--- FINAL DATASET SAMPLE ---")
        print(final_df[['timestamp', 'city', 'temperature_celsius']].head())
        print(final_df[['timestamp', 'city', 'temperature_celsius']].tail())
        
        load_data_to_postgres(final_df)
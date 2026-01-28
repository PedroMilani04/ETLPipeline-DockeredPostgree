import pandas as pd


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
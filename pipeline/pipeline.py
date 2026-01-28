# main.py
import pandas as pd
from utils import get_user_selection
from extract import extract_weather_data
from transform import transform_data
from load import load_data_to_postgres

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
# load.py
from sqlalchemy import create_engine
from config import DB_CONNECTION_URI

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

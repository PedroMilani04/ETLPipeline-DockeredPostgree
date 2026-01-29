import os
import sys

# Caminho para as DLLs do seu ambiente virtual
venv_dll_path = os.path.join(os.getcwd(), "venv", "Lib", "site-packages", "altair", "vegalite", "v5", "plotting")
if os.path.exists(venv_dll_path):
    os.add_dll_directory(venv_dll_path)

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from config import DB_CONNECTION_URI

# 1. Page Configuration
st.set_page_config(
    page_title="Climate Monitoring",
    page_icon="⛈️",
    layout="wide"
)

# 2. Database Connection (With Cache for Performance)
@st.cache_data(ttl=60)  # Updates cache every 60 seconds
def load_data():
    engine = create_engine(DB_CONNECTION_URI)
    # Get most recent data first
    query = "SELECT * FROM weather_forecast ORDER BY timestamp DESC"
    return pd.read_sql(query, engine)

# --- DASHBOARD START ---

st.title("⛈️ Weather Forecast Dashboard")
st.markdown("Real-time ETL pipeline visualization.")

# Load data
try:
    df = load_data()
except Exception as e:
    st.error(f"Error connecting to database: {e}")
    # Stop prevents code from continuing and breaking below
    st.stop() 

# 3. Extra security check
if df is None or df.empty:
    st.warning("Database is empty or returned nothing! Run pipeline.py first.")
    st.stop()

# 3. Sidebar Filters
st.sidebar.header("Filters")
available_cities = df['city'].unique()
selected_city = st.sidebar.selectbox("Select City:", available_cities)

# Filter the DataFrame
filtered_df = df[df['city'] == selected_city]

# 4. KPIs (Top Cards)
# Get the first row (most recent forecast due to ORDER BY)
current = filtered_df.iloc[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Temperature", f"{current['temperature_celsius']} °C")
col2.metric("Humidity", f"{current['relative_humidity']}%")
col3.metric("Wind", f"{current['wind_speed_kmh']} km/h")

# Rain Alert (Conditional Logic)
rain = current['precipitation_mm']
if rain > 0:
    col4.error(f"☔ Rain: {rain} mm")
else:
    col4.success("☀️ No Rain")

# 5. Charts
st.divider()

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("🌡️ Temperature Variation")
    # Simple Streamlit line chart
    st.line_chart(filtered_df, x="timestamp", y="temperature_celsius")

with col_chart2:
    st.subheader("💧 Precipitation (Rain)")
    st.bar_chart(filtered_df, x="timestamp", y="precipitation_mm")

# 6. Raw Data (Optional)
with st.expander("View Raw Data (Table)"):
    st.dataframe(filtered_df)

# Manual refresh button
if st.button('🔄 Refresh Data'):
    st.cache_data.clear() # Clear cache to force new query
    st.rerun()
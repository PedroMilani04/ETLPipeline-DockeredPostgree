# End-to-End Weather Data Pipeline with Python and PostgreSQL

This repository contains a complete **ETL (Extract, Transform, Load) pipeline** solution designed to ingest, process, and persist meteorological data. It implements a modern data engineering workflow, focusing on infrastructure isolation via Docker, efficient data transformation with `pandas`, and robust storage using PostgreSQL.

!(./assets/img.png)

---

## Project Overview

The primary objective of this project is to simulate a production-ready data ingestion environment. It moves beyond simple scripting by incorporating containerization and structured database modeling to handle multi-city weather forecasts.

1.  **Infrastructure as Code (Docker & PostgreSQL)**
    Instead of a local installation, the database infrastructure is provisioned using **Docker Compose**. An isolated container running `postgres:15` is deployed with persistent volumes, ensuring a clean, reproducible, and OS-agnostic development environment—a mandatory standard in modern data engineering.

2.  **Data Extraction (API Integration)**
    Raw weather data is fetched from the **Open-Meteo API**. The pipeline supports dynamic parameters to request specific metrics (temperature, humidity, precipitation, wind speed) for a user-defined list of cities (e.g., São Paulo, London, Tokyo), handling HTTP requests and JSON parsing efficiently.

3.  **Data Transformation & Cleansing (`pandas`)**
    Raw JSON responses are processed into structured DataFrames. Key transformation steps include:
    * Converting ISO 8601 timestamps to Python `datetime` objects.
    * Renaming API keys to database-friendly `snake_case` formats.
    * **Enrichment:** Injecting a categorical `city` column to allow for geographical aggregation and filtering in the database.
    * Consolidating data from multiple locations into a single unified dataset.

4.  **Database Loading (`sqlalchemy`)**
    The transformed data is loaded into the `weather_forecast` table in PostgreSQL. The pipeline utilizes `sqlalchemy` as an ORM (Object Relational Mapper) to handle the connection and schema definition, automatically mapping Python data types to SQL types (e.g., `float64` to `DOUBLE PRECISION`, `datetime` to `TIMESTAMP`).

---

## Database Schema

The pipeline automatically provisions and populates the `weather_forecast` table with the following schema:

| Column | Type | Description |
| :--- | :--- | :--- |
| `timestamp` | TIMESTAMP | Observation date and time |
| `temperature_celsius` | FLOAT | Air temperature at 2 meters |
| `relative_humidity` | FLOAT | Relative humidity percentage |
| `precipitation_mm` | FLOAT | Total precipitation (rain/showers) |
| `wind_speed_kmh` | FLOAT | Wind speed at 10 meters |
| `city` | VARCHAR | Name of the city (Categorical Key) |

---

## Key Learning Outcomes & Features

1.  **Containerization Mastery**
    Practical application of **Docker** to spin up database services. This demonstrates the ability to manage dependencies and isolate environments, preventing "it works on my machine" issues common in data projects.

2.  **Robust ETL Architecture**
    Implementation of a modular pipeline that clearly separates concerns: Extraction (API calls), Transformation (Pandas logic), and Loading (Database transactions). This modularity ensures the code is maintainable and scalable.

3.  **Data Type Handling & Standardization**
    Proficiency in mapping disparate data formats. The project handles the conversion of web-based JSON formats into strict SQL schema requirements, ensuring data integrity across columns like `relative_humidity` and `precipitation_mm`.

4.  **SQL & Python Integration**
    Mastery of using Python as a control plane for database operations. By using `sqlalchemy` engines, the project bridges the gap between object-oriented programming and relational database management systems (RDBMS).

---

## Libraries Used

-   `requests` – for handling HTTP requests to the Open-Meteo API
-   `pandas` – for high-performance data manipulation, cleaning, and aggregation
-   `sqlalchemy` – for establishing the ORM connection between Python and PostgreSQL
-   `psycopg2-binary` – the PostgreSQL adapter for Python
-   `python-dotenv` – for managing environment variables and database credentials securely

---

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/weather-etl-pipeline.git](https://github.com/YOUR_USERNAME/weather-etl-pipeline.git)
    cd weather-etl-pipeline
    ```

2.  **Start the Infrastructure:**
    ```bash
    docker compose up -d
    ```

3.  **Set up the Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

4.  **Execute the Pipeline:**
    ```bash
    python pipeline.py
    ```

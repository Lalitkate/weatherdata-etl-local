# Weather Data ETL - Local

## Project Overview

This project demonstrates a Python-based ETL (Extract, Transform, Load) pipeline that automates the retrieval of historical weather data for major Indian cities using the [WeatherAPI](https://www.weatherapi.com/). The data is transformed into structured daily and hourly formats using `pandas` and then loaded into a local Microsoft SQL Server database.

> ⚠️ Note: This ETL pipeline runs locally and is intended for development or on-premise setups. You can schedule it using tools like Task Scheduler or cron to run daily.

---

## Features

- Extracts weather data (daily and hourly) for 60+ Indian cities.
- Uses the `WeatherAPI` to fetch historical weather data.
- Parses and transforms JSON data into structured pandas DataFrames.
- Automatically inserts the data into SQL Server tables: `daily_weather` and `hourly_weather`.
- Designed to run once daily for the **previous day's** data.
- Easily extensible for other locations, date ranges, or storage systems.

---

## Technologies Used

- Python 3.x
- pandas
- requests
- SQLAlchemy
- pyodbc
- Microsoft SQL Server
- WeatherAPI

---

## Directory Structure

```
weatherdata-etl-local/
│
├── weather_etl.py             # Main ETL script
├── schema.sql                 # SQL schema for target tables
├── requirements.txt           # Python dependencies
├── Weather Data ETL.png       # Solution architecture diagram
└── README.md                  # Project documentation
```

---

## How It Works

1. **Extract**  
   Calls the WeatherAPI for each city in the list using the `history.json` endpoint for **yesterday’s date**.

2. **Transform**  
   - Normalizes the JSON response using `pandas.json_normalize`.
   - Extracts relevant columns for both **daily** and **hourly** datasets.
   - Performs data type conversion for numeric, string, and datetime fields.

3. **Load**  
   - Connects to the local SQL Server using `SQLAlchemy`.
   - Loads `df_daily` and `df_hourly` into respective tables using `to_sql`.

---

## Prerequisites

- Python 3.8 or above
- Microsoft SQL Server (local)
- ODBC Driver 17 or 18 for SQL Server
- WeatherAPI key ([Sign up here](https://www.weatherapi.com/signup.aspx))

---

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Lalitkate/weatherdata-etl-local.git
   cd weatherdata-etl-local
   ```

2. **Install Required Packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Your Configurations**
   - Open `weather_etl.py`
   - Add your `WeatherAPI` key
   - Modify the SQL Server credentials and instance name if required

4. **Create SQL Tables**
   Use the provided `schema.sql` file to create the necessary tables:
   ```sql
   -- daily_weather and hourly_weather tables as defined
   ```

5. **Run the ETL Script**
   ```bash
   python weather_etl.py
   ```

6. **Schedule Automation (Optional)**
   - Windows: Use Task Scheduler
   - Linux/macOS: Use cron jobs

---

## SQL Table Schemas

**`daily_weather`**  
Stores daily weather stats like temperature, humidity, wind, sunrise/sunset, etc.

**`hourly_weather`**  
Stores hourly observations including temperature, wind speed, precipitation, condition, etc.

Check `schema.sql` file for detailed DDL.

---

## Solution Architecture

![Weather Data ETL](Weather%20Data%20ETL.png)

---

## Customization

- Change the list of cities to your desired location(s).
- Modify the date range logic for custom historical backfills.
- Switch database engines (e.g., PostgreSQL, MySQL) using SQLAlchemy.

---

## Disclaimer

This project is for educational/demo purposes. Please review the [WeatherAPI terms](https://www.weatherapi.com/terms.aspx) before using it for commercial applications.

---

## Author

**Lalit Kate**  
Aspiring Data Engineer | Python | Power BI | SQL | Azure | Microsoft Fabric | Databrics

---

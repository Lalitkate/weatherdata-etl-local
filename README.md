# Historical Weather ETL Pipeline for Indian Cities

## Overview
This project builds an automated ETL (Extract, Transform, Load) pipeline to collect **daily and hourly weather data** from [WeatherAPI](https://www.weatherapi.com/) for major Indian cities. The data is transformed using `pandas` and stored into a Microsoft SQL Server database hosted locally.

## Objective
To automate the ingestion, transformation, and storage of weather data that can later be used for analysis, visualization, and climate-related insights for Indian regions.

## Tech Stack
- **Language:** Python  
- **Libraries:** `pandas`, `requests`, `sqlalchemy`, `pyodbc`, `datetime`, `pytz`  
- **Database:** Microsoft SQL Server (local/on-prem)  
- **Data Source:** WeatherAPI (RESTful JSON API)

## ETL Workflow

### 1. Extract
- Connects to the WeatherAPI to fetch weather data for over 60 Indian cities.
- Captures both **daily** and **hourly** weather data for the previous day.

### 2. Transform
- Normalizes JSON responses using `pandas.json_normalize()`.
- Converts relevant columns to appropriate data types (numeric, string, datetime).
- Adds city metadata (name, latitude, longitude).

### 3. Load
- Uses SQLAlchemy to establish a connection to a local SQL Server database.
- Appends the transformed data to the respective tables:
  - `daily_weather`
  - `hourly_weather`

## Cities Covered
Includes a comprehensive list of major Indian cities such as:

`Mumbai, Delhi, Bangalore, Hyderabad, Chennai, Kolkata, Ahmedabad, Jaipur, Lucknow, Bhopal, Patna, Raipur, Bhubaneswar, Ranchi, Thiruvananthapuram, Panaji, Chandigarh, Dehradun, Shimla, Srinagar, Jammu, Dispur, Itanagar, Shillong, Agartala, Aizawl, Imphal, Kohima, Gangtok, Puducherry, Port Blair, Kavaratti, Daman, Leh, Pune, Surat, Indore, Kanpur, Nagpur, Vadodara, Coimbatore, Varanasi, Amritsar, Noida, Ghaziabad, Faridabad, Gurgaon, Mysore, Visakhapatnam, Guwahati, Jodhpur, Allahabad, Meerut, Rajkot, Jabalpur, Ludhiana, Nasik, Trichy, Madurai`

## Configuration
Update the following before running:
- WeatherAPI Key
- SQL Server hostname, username, password, and database name
- List of cities (optional for customization)

## Scheduling
This ETL pipeline is designed to run **once daily** and can be scheduled via:
- Windows Task Scheduler
- CRON (Linux/Mac)
- Orchestration tools like Apache Airflow (for cloud or production deployments)

## Output Tables

### daily_weather
Contains daily metrics such as:
- Max, Min, and Average Temperature (Celsius and Fahrenheit)
- Total Precipitation
- Average Visibility
- Humidity
- Sunrise/Sunset, Moonrise/Moonset
- Location metadata

### hourly_weather
Contains hourly metrics such as:
- Temperature
- Cloud cover
- Wind speed and direction
- Pressure, Humidity
- Rain prediction (chance and probability)
- Weather condition and icon

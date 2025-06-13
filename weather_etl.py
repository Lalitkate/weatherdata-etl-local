# Historical Weather ETL Pipeline for Indian Cities - 

"""
Objective:
This script extracts daily and hourly weather data for major Indian cities using the WeatherAPI,
transforms the data using pandas, and loads it into an on-premises Microsoft SQL Server database.
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import pytz
from sqlalchemy.engine import create_engine, URL

# Define list of cities
location = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow",
    "Bhopal", "Patna", "Raipur", "Bhubaneswar", "Ranchi", "Thiruvananthapuram", "Panaji", "Chandigarh",
    "Dehradun", "Shimla", "Srinagar", "Jammu", "Dispur", "Itanagar", "Shillong", "Agartala", "Aizawl",
    "Imphal", "Kohima", "Gangtok", "Puducherry", "Port Blair", "Kavaratti", "Daman", "Leh", "Pune", "Surat",
    "Indore", "Kanpur", "Nagpur", "Vadodara", "Coimbatore", "Varanasi", "Amritsar", "Noida", "Ghaziabad",
    "Faridabad", "Gurgaon", "Mysore", "Visakhapatnam", "Guwahati", "Jodhpur", "Allahabad", "Meerut",
    "Rajkot", "Jabalpur", "Ludhiana", "Nasik", "Trichy", "Madurai"]

# API base and key
base_url = "http://api.weatherapi.com/v1"
key = ""  # Insert your API key here

# Get yesterday's date in IST (NOTE: YOU CAN USE YOUR DATERANGE)
timezone = pytz.timezone('Asia/Kolkata')
yesterday_date = (datetime.now(timezone) - timedelta(days=1)).date()

# Dictionary to store API responses
weather_dict = {}

for loc in location:
    history_weather_url = f"{base_url}/history.json"
    params = {'key': key, 'q': loc, 'dt': yesterday_date, 'end_dt': yesterday_date}
    response = requests.get(history_weather_url, params=params)
    if response.status_code == 200:
        weather_dict[loc] = response.json()
    else:
        print(response.status_code)
        print(loc, response.text)

# Parse and transform daily weather data
daylist = []

for city, data in weather_dict.items():
    df = pd.json_normalize(data['forecast']['forecastday'])
    df = df[['date','day.maxtemp_c','day.mintemp_c','day.avgtemp_c','day.maxtemp_f','day.mintemp_f','day.avgtemp_f',
            'day.totalprecip_mm','day.avgvis_km','day.uv','day.maxwind_kph','day.avghumidity',
            'astro.sunrise','astro.sunset','astro.moonrise','astro.moonset','day.totalsnow_cm']]
    df['location'] = city
    df['latitude'] = data['location']['lat']
    df['longitude'] = data['location']['lon']
    daylist.append(df)

# Combine daily data into a single DataFrame
df_daily = pd.concat(daylist, ignore_index=True)

# Rename columns
df_daily.rename(columns={
    'day.maxtemp_c': 'maxtemp_c', 'day.mintemp_c': 'mintemp_c', 'day.avgtemp_c': 'avgtemp_c',
    'day.maxtemp_f': 'maxtemp_f', 'day.mintemp_f': 'mintemp_f', 'day.avgtemp_f': 'avgtemp_f',
    'day.totalprecip_mm': 'totalprecip_mm', 'day.avgvis_km': 'avgvis_km', 'day.uv': 'uv',
    'day.maxwind_kph': 'maxwind_kph', 'day.avghumidity': 'avghumidity',
    'astro.sunrise': 'sunrise', 'astro.sunset': 'sunset', 'astro.moonrise': 'moonrise',
    'astro.moonset': 'moonset', 'day.totalsnow_cm': 'totalsnow_cm'
}, inplace=True)

# Set data types
numeric_cols = ['maxtemp_c', 'mintemp_c', 'avgtemp_c', 'maxtemp_f', 'mintemp_f', 'avgtemp_f',
                'totalprecip_mm', 'avgvis_km', 'uv', 'maxwind_kph', 'avghumidity', 'totalsnow_cm',
                'latitude', 'longitude']
string_cols = ["sunrise", "sunset", "moonrise", "moonset", "location"]

df_daily[numeric_cols] = df_daily[numeric_cols].astype(float)
df_daily[string_cols] = df_daily[string_cols].astype(str)
df_daily['date'] = pd.to_datetime(df_daily['date'], errors='coerce')

# Parse and transform hourly weather data
hourly = []

for city, data in weather_dict.items():
    df = pd.json_normalize(data['forecast']['forecastday'], ['hour'])
    df = df.rename(columns={'time': 'datetime'})
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['date'] = df['datetime'].dt.date
    df['time'] = df['datetime'].dt.time
    df = df[[
        'date', 'time', 'datetime', 'cloud', 'temp_c', 'temp_f', 'is_day', 'wind_kph', 'wind_degree',
        'wind_dir', 'pressure_mb', 'snow_cm', 'humidity', 'precip_mm', 'feelslike_c', 'feelslike_f',
        'vis_km', 'gust_kph', 'uv', 'condition.text', 'condition.icon', 'will_it_rain', 'chance_of_rain']]
    df['location'] = city
    df['latitude'] = data['location']['lat']
    df['longitude'] = data['location']['lon']
    hourly.append(df)

# Combine hourly data
df_hourly = pd.concat(hourly, ignore_index=True)

# Rename columns
df_hourly.rename(columns={"condition.text": "condition", "condition.icon": "icon"}, inplace=True)

# Set data types
numeric_cols = ['cloud', 'temp_c', 'temp_f', 'is_day', 'wind_kph', 'wind_degree', 'pressure_mb',
                'snow_cm', 'humidity', 'precip_mm', 'feelslike_c', 'feelslike_f', 'uv', 'vis_km',
                'gust_kph', 'will_it_rain', 'chance_of_rain', 'latitude', 'longitude']
string_cols = ["time", "condition", "icon", "location"]

df_hourly[numeric_cols] = df_hourly[numeric_cols].astype(float)
df_hourly[string_cols] = df_hourly[string_cols].astype(str)
df_hourly['date'] = pd.to_datetime(df_hourly['date'], errors='coerce')

# SQL Server connection
server = "" # Insert your server name.
database = "" # Insert your database name.
username = "" # Insert username.
password = "" # Insert password.

connection_url = URL.create(
    "mssql+pyodbc",
    username=username,
    password=password,
    host=server,
    database=database,
    query={"driver": "ODBC Driver 17 for SQL Server", "TrustServerCertificate": "yes"}
)

engine = create_engine(connection_url, fast_executemany=True)

# Load DataFrames into SQL Server
df_daily.to_sql('daily_weather', con=engine, if_exists='append', index=False)
df_hourly.to_sql('hourly_weather', con=engine, if_exists='append', index=False)

print("ETL process completed!")
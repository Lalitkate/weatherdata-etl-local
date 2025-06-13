/* SQL Code to create 'daily_weather' table */

CREATE TABLE dbo.daily_weather (
    date DATE,
    location VARCHAR(100),
	latitude FLOAT,
	longitude FLOAT,
    maxtemp_c FLOAT,
    mintemp_c FLOAT,
    avgtemp_c FLOAT,
    maxtemp_f FLOAT,
    mintemp_f FLOAT,
    avgtemp_f FLOAT,
    totalprecip_mm FLOAT,
    avgvis_km FLOAT,
    uv FLOAT,
    maxwind_kph FLOAT,
    avghumidity FLOAT,
	totalsnow_cm FLOAT,
    sunrise VARCHAR(20),
    sunset VARCHAR(20),
	moonset VARCHAR(20),
	moonrise VARCHAR(20)
);

/* SQL Code to create 'hourly_weather' table */

CREATE TABLE dbo.hourly_weather (
    date DATE,
	time VARCHAR(20),
	datetime datetime,
    location VARCHAR(100),
	latitude FLOAT,
	longitude FLOAT,
    cloud FLOAT,
    temp_c FLOAT,
	temp_f FLOAT,
    is_day FLOAT,
    wind_kph FLOAT,
    wind_degree FLOAT,
	wind_dir VARCHAR(20),
    pressure_mb FLOAT,
	snow_cm FLOAT,
    humidity FLOAT,
	precip_mm FLOAT,
    feelslike_c FLOAT,
	feelslike_f FLOAT,
    vis_km FLOAT,
    gust_kph FLOAT,
    uv FLOAT,
    condition VARCHAR(200),
    icon VARCHAR(50),
	will_it_rain FLOAT,
	chance_of_rain FLOAT
);
from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor
import json
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import pandas as pd
import requests
import pytz

def convert_time(times):
    eat = pytz.timezone('Africa/Nairobi')
    date_convert = datetime.fromtimestamp(times,tz=eat)    
    return date_convert

def split_Datetime(times):
    return times.strftime("%H:%M:%S")

def weather_data(url):
    #connecting to the weather platform using request function
    data=url.xcom_pull(task_ids="extract_weather_data")
    country_code = data['sys']['country'] #country
    city = data['name'] #city
    sunrise = data['sys']['sunrise'] + data['timezone'] #city timezone (sunrise)
    sunset = data['sys']['sunset'] + data['timezone'] #city timezone (sunset)
    curr_temp = data['main']['feels_like'] - 273.15 #Current temperature
    max_temp = data['main']['temp_max'] - 273.15 # Max temperature
    min_temp = data['main']['temp_min'] - 273.15#Min temperature
    humidity = data['main']['humidity'] #Humidity--check what it means
    pressure = data['main']['pressure']#Pressure---check meaning
    wind_speed = data['wind']['speed']#wind speed        
    clouds = data['clouds']['all'] #clouds
    visibility = data['visibility'] #visibility---check meaning
    precipitation = data['weather'][0]['description'] #weather
    time_recorded = data['dt'] + data['timezone'] #lastupdate

    #converting time to local time
    sunrise_cvt = convert_time(sunrise)
    sunrise_cvt_tim = split_Datetime(sunrise_cvt)
    sunset_cvt = convert_time(sunset)
    sunset_cvt_tim = split_Datetime(sunset_cvt)
    time_recorded_cvt = convert_time(time_recorded)

    #create a dictionary
    data_dict = [{
        'country code': country_code,
        'city': city,
        'sunrise': sunrise_cvt,
        'sunrise_time': sunrise_cvt_tim,
        'sunset' : sunset_cvt,
        'sunset_time': sunset_cvt_tim,
        'temperature' : curr_temp,
        'max_temp' : max_temp,
        'min_temp' : min_temp,
        'humidity' : humidity,
        'pressure' : pressure,
        'wind speed' : wind_speed,
        'clouds' : clouds,
        'visibility' : visibility,
        'precipitation': precipitation,
        'Time recorded': time_recorded_cvt
    }]

    df = pd.DataFrame(data_dict)
    wind_descr = []
    for i in df['wind speed']:
        if i==0:
            i = 'Calm:	Smoke rises vertically'
            wind_descr.append(i)
        elif i>=0.5 and i<=1.5:
            i = 'Light air:	Smoke drifts with air, weather vanes inactive'
            wind_descr.append(i)
        elif i>1.5 and i<=3:
            i = 'Light breeze: Weather vanes active, wind felt on face, leaves rustle'
            wind_descr.append(i)
        elif i>3 and i<=5:
            i = 'Gentle  breeze: Leaves & small twigs move, light flags extend'
            wind_descr.append(i)
        elif i>5 and i<=8:
            i = 'Moderate breeze: Small branches sway, dust & loose paper blows about'
            wind_descr.append(i)
        elif i>8 and i<=10.5:
            i = 'Fresh breeze: Small trees sway, waves break on inland waters'
            wind_descr.append(i)
        elif i>10.5 and i<=13.5:
            i = 'Strong breeze: Large branches sway, umbrellas difficult to use'
            wind_descr.append(i)
        elif i>13.5 and i<=16.5:
            i = 'Moderate gale: Whole trees sway, difficult to walk against wind'
            wind_descr.append(i)
        elif i>16.5 and i<=20:
            i = 'Fresh gale: Twigs broken off trees, walking against wind very difficult'
            wind_descr.append(i)
        elif i>20 and i<=23.5:
            i = 'Strong gale: Slight damage to buildings, shingles blown off roof'
            wind_descr.append(i)
        elif i>23.5 and i<=27.5:
            i = 'Whole gale: Trees uprooted, considerable damage to buildings'
            wind_descr.append(i)
        elif i>27.5 and i<=31.5:
            i = 'Storm: Widespread damage, very rare occurrence'
            wind_descr.append(i)
        else:
            i = 'Hurricane: Violent destruction'
            wind_descr.append(i)
    df['wind description'] = wind_descr
   
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    dt_string = 'current_weather_nairobi_' + dt_string
    df.to_csv(f"s3://weatherbucket123/{dt_string}.csv", index=False, storage_options=aws_credentials)

# creating dags confs

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 22),
    'email': ['castrooyoo@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

with DAG('weather_dag',
        default_args=default_args,
        schedule_interval = '@daily',
        catchup=False) as dag:

        #connecting the source to my dag
        is_weather_api_ready = HttpSensor(
        task_id ='is_weather_api_ready',
        http_conn_id='curr_weather_api',
        endpoint='/data/2.5/weather?q=Nairobi&appid=8c517a3e9d8b5dec9a6dd2e7f61ac74d'
        )

        extract_weather_data = SimpleHttpOperator(
        task_id = 'extract_weather_data',
        http_conn_id = 'curr_weathermap_api',
        endpoint='/data/2.5/weather?q=Nairobi&appid=8c517a3e9d8b5dec9a6dd2e7f61ac74d',
        method = 'GET',
        response_filter= lambda r: json.loads(r.text),
        log_response=True
        )

        transform_load_weather_data = PythonOperator(
        task_id= 'transform_load_weather_data',
        python_callable=weather_data
        )

        is_weather_api_ready >> extract_weather_data >> transform_load_weather_data
from django.test import TestCase
from datetime import *
from calendar import *
from os import environ
import requests
import time
import pandas as pd
import json

# Create your tests here.



def get_current_day_day(date):
    date = pd.Timestamp(date)
    print(date)
    
    
date3 = "2022-24-11"
get_current_day_day(date3)





now = datetime.now()

current_year = now.year
current_day = now.day
current_month = now.month
current_weekday = now.weekday()

weekdays = {
    0 : 'Monday', 
    1 : 'Tuesday', 
    2 : 'Wednesday',
    3 : 'Thursday',
    4 : 'Friday',
    5 : 'Saturday',
    6 : 'Sunday'
}

print("Today's Date: " + weekdays[current_weekday])

print()

list_weekdays = []
for day in weekdays.values():
    list_weekdays.append(day)
    
day = int(current_weekday) + 1
next5days = list_weekdays[day:7]

# print(next5days)

# next_day1 = next5days[0]
# next_day2 = next5days[1]
# next_day3 = next5days[2]
# next_day4 = next5days[3]
# next_day5 = next5days[4]

# print(next_day1, next_day2, next_day3, next_day4, next_day5)



def get_current_day_weather(city="Arlington", units="imperial"):
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = environ.get("CEJ_Weather_API")
    CITY = city
    UNITS = units
    
    first_api_call = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units={UNITS}"
    
    response1 = requests.get(first_api_call).json()
    response1_prettyprint = json.dumps(response1, indent=3)
    
    get_weather_report = response1["weather"][0]["main"] # Clouds
    current_temp = response1["main"]['temp'] # current temperature
    min_temp = response1["main"]["temp_min"] # temperature low
    max_temp = response1["main"]["temp_max"] # temperature high
    humidity = response1["main"]["humidity"] # humidity
    wind_speed = str(response1["wind"]["speed"]).split(".")[0] # wind speed
    wind_direction = int(response1["wind"]["deg"]) # wind direction in degrees, pass into calculate_wind()
    
    
    sector = {
        1 : "North",
        2 : "North North East",
        3 : "North East",
        4 : "East North East",
        5 : "East",
        6 : "East South East",
        7 : "South East",
        8 : "South South East",
        9 : "South",
        10 : "South South West",
        11 : "South West",
        12 : "West South West",
        13 : "West",
        14 : "West North West",
        15 : "North West",
        16 : "North North West",
        17 : "North",        
        }
    degrees = wind_direction
    Index = int(degrees) % 360
    Index = round(Index/ 22.5,0) + 1
    CompassDir = sector[Index]
    
    
    
    LAT = len(str(response1['coord']['lat']))
    if LAT == 7:
        LAT = str(response1['coord']['lat'])[0:5]
    else:
        LAT = str(response1['coord']['lat'])[0:6]
        
    LON = len(str(response1["coord"]["lon"]))
    if LON == 7:
        LON = str(response1["coord"]["lon"])[0:5]
    else:
        LON = str(response1["coord"]["lon"])[0:6]
        
        
        
    return get_weather_report, current_temp, min_temp, max_temp, humidity, wind_speed, CompassDir, LON, LAT
        
    
    
    
    
    
    
def weather_next_few_hours(lat, lon, units="imperial"):
    api_key = environ.get("CEJ_Weather_API")
    LAT = lat
    LON = lon
    UNITS = units
    
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={api_key}&units={UNITS}"
    response = requests.get(url).json()
    response_prettyprint = json.dumps(response, indent=3)
    
    
    today_3pm = response['list'][0]
    today_6pm = response['list'][1]
    today_9pm = response['list'][2]
    
    
    today_3pm_min_temp = str(today_3pm['main']['temp_min']).split('.')[0]
    today_3pm_max_temp = str(today_3pm['main']['temp_max']).split('.')[0]
    today_3pm_weather = str(today_3pm['weather'][0]['description'])
    
    today_6pm_min_temp = str(today_6pm['main']['temp_min']).split('.')[0]
    today_6pm_max_temp = str(today_6pm['main']['temp_max']).split('.')[0]
    today_6pm_weather = str(today_6pm['weather'][0]['description'])
    
    today_9pm_min_temp = str(today_9pm['main']['temp_min']).split('.')[0]
    today_9pm_max_temp = str(today_9pm['main']['temp_max']).split('.')[0]
    today_9pm_weather = str(today_9pm['weather'][0]['description'])
    
    return [today_3pm_min_temp, today_3pm_max_temp, today_3pm_weather, today_6pm_max_temp, today_6pm_min_temp, today_6pm_weather, today_9pm_max_temp, today_9pm_min_temp, today_9pm_weather]




current_day_weather = get_current_day_weather()[0]
current_day_temp = get_current_day_weather()[1]
current_day_min_temp = get_current_day_weather()[2]
current_day_max_temp = get_current_day_weather()[3]
current_day_humidity = get_current_day_weather()[4]
current_day_wind_speed = get_current_day_weather()[5]
current_day_wind_dir = get_current_day_weather()[6]
cc_lon = get_current_day_weather()[7]
cc_lat = get_current_day_weather()[8]

units = "imperial"




def coming_days(lat, lon, units="imperial"):
    api_key = environ.get("CEJ_Weather_API")
    LAT = lat
    LON = lon
    UNITS = units
    
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={api_key}&units={UNITS}"
    response = requests.get(url).json()
    response_prettyprint = json.dumps(response, indent=3)
    
    
    
    # Tomorrows Weather Forcast
    current_day_plus_1 = response['list'][3]
    tomorrow_min_temp = str(current_day_plus_1['main']['temp_min']).split('.')[0]
    tomorrow_max_temp = str(current_day_plus_1['main']['temp_max']).split('.')[0]
    tomorrow_weather = str(current_day_plus_1['weather'][0]['description'])
    tomorrows_date = str(current_day_plus_1['dt_txt'])

        
    # Two days from current dates forcast
    current_day_plus_2 = response['list'][11]
    day2_min_temp = str(current_day_plus_2['main']['temp_min']).split('.')[0]
    day2_max_temp = str(current_day_plus_2['main']['temp_max']).split('.')[0]
    day2_weather = str(current_day_plus_2['weather'][0]['description'])
    day2_date = str(current_day_plus_2['dt_txt'])
    
    
    # Three days from current dates forcast
    current_day_plus_3 = response['list'][19]
    day3_min_temp = str(current_day_plus_3['main']['temp_min']).split('.')[0]
    day3_max_temp = str(current_day_plus_3['main']['temp_max']).split('.')[0]
    day3_weather = str(current_day_plus_3['weather'][0]['description'])
    day3_date = str(current_day_plus_3['dt_txt'])
    
    
    # Four days from current dates forcast
    current_day_plus_4 = response['list'][27]
    day4_min_temp = str(current_day_plus_4['main']['temp_min']).split('.')[0]
    day4_max_temp = str(current_day_plus_4['main']['temp_max']).split('.')[0]
    day4_weather = str(current_day_plus_4['weather'][0]['description'])
    day4_date = str(current_day_plus_4['dt_txt'])
    
    
    # Five days from current dates forcast
    current_day_plus_5 = response['list'][35]
    day5_min_temp = str(current_day_plus_5['main']['temp_min']).split('.')[0]
    day5_max_temp = str(current_day_plus_5['main']['temp_max']).split('.')[0]
    day5_weather = str(current_day_plus_5['weather'][0]['description'])
    day5_date = str(current_day_plus_5['dt_txt'])
    
    return {
        "day1": [tomorrow_weather, tomorrow_max_temp, tomorrow_min_temp, tomorrows_date],
        "day2": [day2_weather, day2_max_temp, day2_min_temp, day2_date],
        "day3": [day3_weather, day3_max_temp, day3_min_temp, day3_date],
        "day4": [day4_weather, day4_max_temp, day4_min_temp, day4_date],
        "day5": [day5_weather, day5_max_temp, day5_min_temp, day5_date],
        }
    



j = coming_days(cc_lat, cc_lon, units)

print(j)

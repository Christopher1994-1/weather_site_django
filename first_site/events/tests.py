from django.test import TestCase
from datetime import *
from calendar import *
from os import environ
import requests
import time
import json

# Create your tests here.
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


def calculate_wind(degrees):
    """a function that takes in the wind degrees INT and calculates it to compass direction

    Args:
        degrees (INT): the direction degrees

    Returns:
        str: the final calculated result converted from degrees to compass direction
    """
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
    Index = int(degrees) % 360
    Index = round(Index/ 22.5,0) + 1
    CompassDir = sector[Index]
    return CompassDir


def get_weather(city="Arlington", units="imperial"):
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
        
    
    # TODO plan is to have this API call for hourly and another for daily ones with logic built in so that we know
    # if current hour still have indexes and daily is +1 more than today, also put each into its own function
    hourly_url =f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&cnt=3&appid={API_KEY}&units={UNITS}"
    response2 = requests.get(hourly_url).json()
    response2_prettyprint = json.dumps(response2, indent=3)
    
    
    epoch_time_day_1 = response2["list"][0]["dt"]
    day_one = time.strftime('%Y-%m-%d', time.localtime(int(epoch_time_day_1)))
    day_one_weather = response2["list"][0]["weather"][0]["main"] # clouds
    day_one_min_temp = str(response2["list"][0]["main"]["temp_min"]).split(".")[0] # temp low
    day_one_max_temp = str(response2["list"][0]["main"]["temp_max"]).split(".")[0] # temp high
    
    
    current_day_18hr = response2["list"]
    # current_day_21hr = response2["list"][1]
    # current_day_21hrj = response2["list"][2]
    # epoch_time_day_3 = response2["list"][29]
    

    
    
    
    print(current_day_18hr)
    # print()
    # print(current_day_21hr)
    # print()
    # print(current_day_21hrj)
    # print()
    # print(epoch_time_day_4)
    # print()
    # print(epoch_time_day_5)
    # print()
    # print(epoch_time_day_6)
    # print()
    # print(epoch_time_day_7)
    # print()
    # print(epoch_time_day_8)
    # print()
    # print(epoch_time_day_9)
    # print()
    # print(epoch_time_day_10)
    # print()
    
    


get_weather()
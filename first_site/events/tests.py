from django.test import TestCase
from datetime import *
from calendar import *
from os import environ
import requests
import time
import json

# Create your tests here.



def get_next_day():
    
    now = datetime.now()
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

    next_day = weekdays[current_weekday]
    
    if next_day == "Monday":
        next_five_days = ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
    elif next_day == "Tuesday":
        next_five_days = ["Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Monday"]
        
    elif next_day == "Wednesday":
        next_five_days = ["Thursday", "Friday", "Saturday", "Sunday", "Monday", "Tuesday"]
        
    elif next_day == "Thursday":
        next_five_days = ["Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday"]

    elif next_day == "Friday":
        next_five_days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
        
    elif next_day == "Saturday":
        next_five_days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        
    elif next_day == "Sunday":
        next_five_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        
    return next_five_days





def get_current_day_weather(city="Arlington", units="imperial"):
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = environ.get("CEJ_Weather_API")
    CITY = city
    UNITS = units
    
    first_api_call = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units={UNITS}"
    
    response1 = requests.get(first_api_call).json()
    response1_prettyprint = json.dumps(response1, indent=3)
    
    get_weather_report = response1["weather"][0]["description"] # Clouds
    current_temp = response1["main"]['temp'] # current temperature
    min_temp = response1["main"]["temp_min"] # temperature low
    max_temp = response1["main"]["temp_max"] # temperature high
    humidity = response1["main"]["humidity"] # humidity
    wind_speed = str(response1["wind"]["speed"]).split(".")[0] # wind speed
    wind_direction = int(response1["wind"]["deg"]) # wind direction in degrees, pass into calculate_wind()
    city_name = response1["name"]
    visual = response1["visibility"]
    
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
        
    current_date = get_next_day()[1]
        
        
        
    return get_weather_report, current_temp, min_temp, max_temp, humidity, wind_speed, CompassDir, LON, LAT, current_date, visual
        

# k = get_current_day_weather()
# print(k)    

    
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
    
    dt_3pm_dt = str(today_3pm['dt_txt']).split(' ')[0]
    dt_3pm_month = dt_3pm_dt.split('-')[1] # thing to return
    dt_3pm_day = dt_3pm_dt.split('-')[2] # thing to return
    
    
    
    dt_3pm_time = str(today_3pm['dt_txt']).split(' ')[1]
    dt_3pm_hr = dt_3pm_time.split(':')[0]
    dt_3pm_min = dt_3pm_time.split(':')[1]
    CON3 = dt_3pm_hr + ":" + dt_3pm_min
    
    convert_dt3 = datetime.strptime(CON3,'%H:%M').strftime('%I:%M %p') # thing to return
    
    
    dt_6pm_dt = str(today_6pm['dt_txt']).split(' ')[0]
    dt_6pm_month = dt_6pm_dt.split('-')[1] # thing to return
    dt_6pm_day = dt_6pm_dt.split('-')[2] # thing to return
    
    
    dt_6pm_time = str(today_6pm['dt_txt']).split(' ')[1]
    dt_6pm_hr = dt_6pm_time.split(':')[0]
    dt_6pm_min = dt_6pm_time.split(':')[1]
    CON6 = dt_6pm_hr + ":" + dt_6pm_min
    
    convert_dt6 = datetime.strptime(CON6,'%H:%M').strftime('%I:%M %p') # thing to return
    
    
    dt_9pm_dt = str(today_9pm['dt_txt']).split(' ')[0]
    dt_9pm_month = dt_9pm_dt.split('-')[1] # thing to return
    dt_9pm_day = dt_9pm_dt.split('-')[2] # thing to return
    
    
    dt_9pm_time = str(today_9pm['dt_txt']).split(' ')[1]
    dt_9pm_hr = dt_9pm_time.split(':')[0]
    dt_9pm_min = dt_9pm_time.split(':')[1]
    CON9 = dt_9pm_hr + ":" + dt_9pm_min
    
    convert_dt9 = datetime.strptime(CON9,'%H:%M').strftime('%I:%M %p') # thing to return
    
    
    
    
    today_3pm_min_temp = str(today_3pm['main']['temp_min']).split('.')[0]
    today_3pm_max_temp = str(today_3pm['main']['temp_max']).split('.')[0]
    today_3pm_weather = str(today_3pm['weather'][0]['description'])
    
    today_6pm_min_temp = str(today_6pm['main']['temp_min']).split('.')[0]
    today_6pm_max_temp = str(today_6pm['main']['temp_max']).split('.')[0]
    today_6pm_weather = str(today_6pm['weather'][0]['description'])
    
    today_9pm_min_temp = str(today_9pm['main']['temp_min']).split('.')[0]
    today_9pm_max_temp = str(today_9pm['main']['temp_max']).split('.')[0]
    today_9pm_weather = str(today_9pm['weather'][0]['description'])

    
    return [[dt_3pm_month, dt_3pm_day, convert_dt3, today_3pm_max_temp, today_3pm_min_temp, today_3pm_weather],
            [dt_6pm_month, dt_6pm_day, convert_dt6, today_6pm_max_temp, today_6pm_min_temp, today_6pm_weather],
            [dt_9pm_month, dt_9pm_day, convert_dt9, today_9pm_max_temp, today_9pm_min_temp, today_9pm_weather],]




# current_day_weather = get_current_day_weather()[0]
# current_day_temp = get_current_day_weather()[1]
# current_day_min_temp = get_current_day_weather()[2]
# current_day_max_temp = get_current_day_weather()[3]
# current_day_humidity = get_current_day_weather()[4]
# current_day_wind_speed = get_current_day_weather()[5]
# current_day_wind_dir = get_current_day_weather()[6]
# print(get_current_day_weather()[7])
# print(get_current_day_weather()[8])

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
    tomorrows_day = get_next_day()[0][0]

        
    # Two days from current dates forcast
    current_day_plus_2 = response['list'][11]
    day2_min_temp = str(current_day_plus_2['main']['temp_min']).split('.')[0]
    day2_max_temp = str(current_day_plus_2['main']['temp_max']).split('.')[0]
    day2_weather = str(current_day_plus_2['weather'][0]['description'])
    day2_date = str(current_day_plus_2['dt_txt'])
    day2_day = get_next_day()[0][1]
    
    
    # Three days from current dates forcast
    current_day_plus_3 = response['list'][19]
    day3_min_temp = str(current_day_plus_3['main']['temp_min']).split('.')[0]
    day3_max_temp = str(current_day_plus_3['main']['temp_max']).split('.')[0]
    day3_weather = str(current_day_plus_3['weather'][0]['description'])
    day3_date = str(current_day_plus_3['dt_txt'])
    day3_day = get_next_day()[0][2]
    
    
    # Four days from current dates forcast
    current_day_plus_4 = response['list'][27]
    day4_min_temp = str(current_day_plus_4['main']['temp_min']).split('.')[0]
    day4_max_temp = str(current_day_plus_4['main']['temp_max']).split('.')[0]
    day4_weather = str(current_day_plus_4['weather'][0]['description'])
    day4_date = str(current_day_plus_4['dt_txt'])
    day4_day = get_next_day()[0][3]
    
    
    # Five days from current dates forcast
    current_day_plus_5 = response['list'][35]
    day5_min_temp = str(current_day_plus_5['main']['temp_min']).split('.')[0]
    day5_max_temp = str(current_day_plus_5['main']['temp_max']).split('.')[0]
    day5_weather = str(current_day_plus_5['weather'][0]['description'])
    day5_date = str(current_day_plus_5['dt_txt'])
    day5_day = get_next_day()[0][4]
    
    return {
        "day1": [tomorrow_weather, tomorrow_max_temp, tomorrow_min_temp, tomorrows_date, tomorrows_day],
        "day2": [day2_weather, day2_max_temp, day2_min_temp, day2_date, day2_day],
        "day3": [day3_weather, day3_max_temp, day3_min_temp, day3_date, day3_day],
        "day4": [day4_weather, day4_max_temp, day4_min_temp, day4_date, day4_day],
        "day5": [day5_weather, day5_max_temp, day5_min_temp, day5_date, day5_day],
        }
    





current_weekday = "Thursday"


next_things = get_next_day()

print(next_things)
from django.shortcuts import render, redirect
from datetime import *
from .forms import SubListForm
from django.http import HttpResponseRedirect
import random
from django.contrib import messages
import json
import time
import pytz
from . import codes
import datetime
from os import environ
from . import codes
import requests
from django.contrib import messages


def afternoon():
    now = datetime.datetime.now()
    timeNow = now.hour
    if timeNow < 12:
        return "Morning"
    elif timeNow < 16:
        return "Afternoon"
    elif timeNow < 19:
        return "Evening"
    else:
        return "Night"





# function to call to get the next few weekdays 
def get_next_day(weekday):
    
    next_day = weekday
    
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



# function to call to get data on the current forecast
def get_current_day_weather(city="Arlington"):
    """
    Retrieve current weather data for a given city and return it in either imperial or metric units.

    Parameters:
    - city (str): The name of the city for which to retrieve weather data. Default is "Arlington".
    - units (str): The units in which to return the weather data. Can be either "imperial" (default) or "metric".

    Returns:
    - A dictionary containing the following weather data for the specified city:
        - Main weather condition (str)
        - Weather description (str)
        - Current temperature (str)
        - Minimum temperature (str)
        - Maximum temperature (str)
        - Humidity (str)
        - Wind speed (str)
        - Wind direction (str)
        - City name (str)
        - Visibility (str)
        - Latitude (str)
        - Longitude (str)
    """
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = environ.get("CEJ_Weather_API")
    CITY = city
    
    if CITY == '':
        search_result_false = "None"
        city_name = 'Arlington'
        UNITS = "imperial"
        
        first_api_call = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units={UNITS}"
        
        response1 = requests.get(first_api_call).json()
        

        get_main = response1["weather"][0]["main"] # Main weather report 'Clouds'
        get_weather_des = response1["weather"][0]["description"] # clear sky
        current_temp = response1["main"]['temp'] # current temperature
        current_temp_length = len(str(current_temp).split('.')[0]) # length of current temperature
        min_temp = response1["main"]["temp_min"] # temperature low
        max_temp = response1["main"]["temp_max"] # temperature high
        humidity = response1["main"]["humidity"] # humidity
        wind_speed = str(response1["wind"]["speed"]).split(".")[0] # wind speed
        wind_direction = int(response1["wind"]["deg"]) # wind direction in degrees, pass into calculate_wind()
        city_name = response1["name"]
        visual = response1["visibility"]
            
            
            
        # converting CURRENT TEMP from Fahrenheit to Celsius
        convert_current_temp = int(str(current_temp).split('.')[0])
        metric_current_temp = str((convert_current_temp - 32) * 5/9).split('.')[0]
        current_temp_str = str(current_temp).split('.')[0]
            
            
            
        # converting MIN TEMP from Fahrenheit to Celsius
        convert_min_temp = int(str(min_temp).split('.')[0])
        metric_min_temp = str((convert_min_temp - 32) * 5/9).split('.')[0]
        min_temp_str = str(min_temp).split('.')[0]
        
        
        # converting MAX TEMP from Fahrenheit to Celsius
        convert_max_temp = int(str(max_temp).split('.')[0])
        metric_max_temp = str((convert_max_temp - 32) * 5/9).split('.')[0]
        max_temp_str = str(max_temp).split('.')[0]
        
        
        
        # converting wind speed to metric
        toIntWind = int(wind_speed) * 1.609
        wind_speed_metric = str(toIntWind).split('.')[0]
        
        
        # converting visibility to mph/k
        visual_in_miles = str(int(visual) / 1609.34).split('.')[0]
        visual_in_kilo = str(int(visual_in_miles) * 1.60934).split('.')[0]
            
            

        
        sector = {
            1 : "N",
            2 : "NNE",
            3 : "NE",
            4 : "ENE",
            5 : "E",
            6 : "SSE",
            7 : "SE",
            8 : "SSE",
            9 : "S",
            10 : "SSW",
            11 : "SW",
            12 : "WSW",
            13 : "W",
            14 : "WNW",
            15 : "NW",
            16 : "NNW",
            17 : "N",        
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
    
    
    elif CITY != '' and CITY != 'Arlington':
        search_result_false = "True"
        city_name = CITY
        UNITS = "imperial"
        
        first_api_call = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units={UNITS}"
        
        response1 = requests.get(first_api_call).json()
        
        try:
            search_result_false = "True"
            get_main = response1["weather"][0]["main"] # Main weather report 'Clouds'
            get_weather_des = response1["weather"][0]["description"] # clear sky
            current_temp = response1["main"]['temp'] # current temperature
            current_temp_length = len(str(current_temp).split('.')[0]) # length of current temperature
            min_temp = response1["main"]["temp_min"] # temperature low
            max_temp = response1["main"]["temp_max"] # temperature high
            humidity = response1["main"]["humidity"] # humidity
            wind_speed = str(response1["wind"]["speed"]).split(".")[0] # wind speed
            wind_direction = int(response1["wind"]["deg"]) # wind direction in degrees, pass into calculate_wind()
            city_name = response1["name"]
            visual = response1["visibility"]
                
                
                
            # converting CURRENT TEMP from Fahrenheit to Celsius
            convert_current_temp = int(str(current_temp).split('.')[0])
            metric_current_temp = str((convert_current_temp - 32) * 5/9).split('.')[0]
            current_temp_str = str(current_temp).split('.')[0]
                
                
                
            # converting MIN TEMP from Fahrenheit to Celsius
            convert_min_temp = int(str(min_temp).split('.')[0])
            metric_min_temp = str((convert_min_temp - 32) * 5/9).split('.')[0]
            min_temp_str = str(min_temp).split('.')[0]
            
            
            # converting MAX TEMP from Fahrenheit to Celsius
            convert_max_temp = int(str(max_temp).split('.')[0])
            metric_max_temp = str((convert_max_temp - 32) * 5/9).split('.')[0]
            max_temp_str = str(max_temp).split('.')[0]
            
            
            
            # converting wind speed to metric
            toIntWind = int(wind_speed) * 1.609
            wind_speed_metric = str(toIntWind).split('.')[0]
            
            
            # converting visibility to mph/k
            visual_in_miles = str(int(visual) / 1609.34).split('.')[0]
            visual_in_kilo = str(int(visual_in_miles) * 1.60934).split('.')[0]
                
                

            
            sector = {
                1 : "N",
                2 : "NNE",
                3 : "NE",
                4 : "ENE",
                5 : "E",
                6 : "SSE",
                7 : "SE",
                8 : "SSE",
                9 : "S",
                10 : "SSW",
                11 : "SW",
                12 : "WSW",
                13 : "W",
                14 : "WNW",
                15 : "NW",
                16 : "NNW",
                17 : "N",        
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
                
                
        except KeyError:
            search_result_false = "None"
            city_name = 'Arlington'
            UNITS = "imperial"
            
            first_api_call = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units={UNITS}"
            
            response1 = requests.get(first_api_call).json()


            get_main = response1["weather"][0]["main"] # Main weather report 'Clouds'
            get_weather_des = response1["weather"][0]["description"] # clear sky
            current_temp = response1["main"]['temp'] # current temperature
            current_temp_length = len(str(current_temp).split('.')[0]) # length of current temperature
            min_temp = response1["main"]["temp_min"] # temperature low
            max_temp = response1["main"]["temp_max"] # temperature high
            humidity = response1["main"]["humidity"] # humidity
            wind_speed = str(response1["wind"]["speed"]).split(".")[0] # wind speed
            wind_direction = int(response1["wind"]["deg"]) # wind direction in degrees, pass into calculate_wind()
            city_name = response1["name"]
            visual = response1["visibility"]
                
                
                
            # converting CURRENT TEMP from Fahrenheit to Celsius
            convert_current_temp = int(str(current_temp).split('.')[0])
            metric_current_temp = str((convert_current_temp - 32) * 5/9).split('.')[0]
            current_temp_str = str(current_temp).split('.')[0]
                
                
                
            # converting MIN TEMP from Fahrenheit to Celsius
            convert_min_temp = int(str(min_temp).split('.')[0])
            metric_min_temp = str((convert_min_temp - 32) * 5/9).split('.')[0]
            min_temp_str = str(min_temp).split('.')[0]
            
            
            # converting MAX TEMP from Fahrenheit to Celsius
            convert_max_temp = int(str(max_temp).split('.')[0])
            metric_max_temp = str((convert_max_temp - 32) * 5/9).split('.')[0]
            max_temp_str = str(max_temp).split('.')[0]
            
            
            
            # converting wind speed to metric
            toIntWind = int(wind_speed) * 1.609
            wind_speed_metric = str(toIntWind).split('.')[0]
            
            
            # converting visibility to mph/k
            visual_in_miles = str(int(visual) / 1609.34).split('.')[0]
            visual_in_kilo = str(int(visual_in_miles) * 1.60934).split('.')[0]
                
                

            
            sector = {
                1 : "N",
                2 : "NNE",
                3 : "NE",
                4 : "ENE",
                5 : "E",
                6 : "SSE",
                7 : "SE",
                8 : "SSE",
                9 : "S",
                10 : "SSW",
                11 : "SW",
                12 : "WSW",
                13 : "W",
                14 : "WNW",
                15 : "NW",
                16 : "NNW",
                17 : "N",        
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
            
        
        
    try:
          return  [get_main, get_weather_des, current_temp_str, min_temp_str, max_temp_str, humidity, wind_speed,
                    CompassDir, LON, LAT, visual_in_miles, visual_in_kilo, city_name, metric_current_temp,
                  metric_min_temp, metric_max_temp, wind_speed_metric, current_temp_length, search_result_false]
    except UnboundLocalError:
        return "None"
        
        
          
        

# function to call to get data on the next few hours forecast
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
    
    
    convert_dt3 = datetime.datetime.strptime(CON3,'%H:%M').strftime('%I:%M %p') # thing to return
    
    
    dt_6pm_dt = str(today_6pm['dt_txt']).split(' ')[0]
    dt_6pm_month = dt_6pm_dt.split('-')[1] # thing to return
    dt_6pm_day = dt_6pm_dt.split('-')[2] # thing to return
    
    
    dt_6pm_time = str(today_6pm['dt_txt']).split(' ')[1]
    dt_6pm_hr = dt_6pm_time.split(':')[0]
    dt_6pm_min = dt_6pm_time.split(':')[1]
    CON6 = dt_6pm_hr + ":" + dt_6pm_min
    
    convert_dt6 = datetime.datetime.strptime(CON6,'%H:%M').strftime('%I:%M %p') # thing to return
    
    
    dt_9pm_dt = str(today_9pm['dt_txt']).split(' ')[0]
    dt_9pm_month = dt_9pm_dt.split('-')[1] # thing to return
    dt_9pm_day = dt_9pm_dt.split('-')[2] # thing to return
    
    
    dt_9pm_time = str(today_9pm['dt_txt']).split(' ')[1]
    dt_9pm_hr = dt_9pm_time.split(':')[0]
    dt_9pm_min = dt_9pm_time.split(':')[1]
    CON9 = dt_9pm_hr + ":" + dt_9pm_min
    
    convert_dt9 = datetime.datetime.strptime(CON9,'%H:%M').strftime('%I:%M %p') # thing to return
    
    
    
    # Getting the min temp for the first hour 
    today_3pm_min_temp = str(today_3pm['main']['temp_min']).split('.')[0]
    
    # converting the first hour min temp from Fahrenheit to Celsius
    covert_dt_3pm_min = int(today_3pm_min_temp); m3pm = (covert_dt_3pm_min - 32) * 5/9
    metric_dt_3pm_min = str(m3pm).split('.')[0]
    
    # Getting the max temp for the first hour
    today_3pm_max_temp = str(today_3pm['main']['temp_max']).split('.')[0]
    
    # converting the first hour min temp from Fahrenheit to Celsius
    covert_dt_3pm_max = int(today_3pm_max_temp); max3pm = (covert_dt_3pm_max - 32) * 5/9
    metric_dt_3pm_max = str(max3pm).split('.')[0]
    
    # Getting the weather description
    today_3pm_weather = str(today_3pm['weather'][0]['description'])
    
    ######################################################
    
    # Getting the min temp for the second hour 
    today_6pm_min_temp = str(today_6pm['main']['temp_min']).split('.')[0]
    
    # converting the second hour min temp from Fahrenheit to Celsius
    covert_dt_6pm_min = int(today_6pm_min_temp); m6pm = (covert_dt_6pm_min - 32) * 5/9
    metric_dt_6pm_min = str(m6pm).split('.')[0]
    
    
    # Getting the max temp for the second hour 
    today_6pm_max_temp = str(today_6pm['main']['temp_max']).split('.')[0]
    
    # converting the second hour max temp from Fahrenheit to Celsius
    covert_dt_6pm_max = int(today_6pm_max_temp); max6pm = (covert_dt_6pm_max - 32) * 5/9
    metric_dt_6pm_max = str(max6pm).split('.')[0]
    
    # Getting the weather description
    today_6pm_weather = str(today_6pm['weather'][0]['description'])
    
    ####################################################################
    
    # Getting the min temp for the third hour 
    today_9pm_min_temp = str(today_9pm['main']['temp_min']).split('.')[0]
    
    # converting the second hour min temp from Fahrenheit to Celsius
    covert_dt_9pm_min = int(today_9pm_min_temp); m9pm = (covert_dt_9pm_min - 32) * 5/9
    metric_dt_9pm_min = str(m9pm).split('.')[0]
    
    # Getting the max temp for the third hour 
    today_9pm_max_temp = str(today_9pm['main']['temp_max']).split('.')[0]
    
    # converting the second hour max temp from Fahrenheit to Celsius
    covert_dt_9pm_max = int(today_9pm_max_temp); max9pm = (covert_dt_9pm_max - 32) * 5/9
    metric_dt_9pm_max = str(max9pm).split('.')[0]
    
    # Getting the weather description
    today_9pm_weather = str(today_9pm['weather'][0]['description'])


    return [[dt_3pm_month, dt_3pm_day, convert_dt3, today_3pm_max_temp, today_3pm_min_temp, today_3pm_weather, metric_dt_3pm_min, metric_dt_3pm_max],
            [dt_6pm_month, dt_6pm_day, convert_dt6, today_6pm_max_temp, today_6pm_min_temp, today_6pm_weather, metric_dt_6pm_min, metric_dt_6pm_max],
            [dt_9pm_month, dt_9pm_day, convert_dt9, today_9pm_max_temp, today_9pm_min_temp, today_9pm_weather, metric_dt_9pm_min, metric_dt_9pm_max],]





# function to call to get data on the weekly forecast
def coming_days(lat, lon, units="imperial"):
    api_key = environ.get("CEJ_Weather_API")
    LAT = lat
    LON = lon
    UNITS = units
    
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={api_key}&units={UNITS}"
    response = requests.get(url).json()
    response_prettyprint = json.dumps(response, indent=3)
    
    
    
    # Tomorrows Weather Forcast API Call
    current_day_plus_1 = response['list'][3]
    # Tomorrows Min Temp
    tomorrow_min_temp = str(current_day_plus_1['main']['temp_min']).split('.')[0]
    # Converting First Day min temp to celisus 
    convert_to_celisus_day1 = int(tomorrow_min_temp); day1_calculations = (convert_to_celisus_day1 - 32) * 5/9
    day1_min_metric = str(day1_calculations).split('.')[0]
    # Tomorrows Max Temp
    tomorrow_max_temp = str(current_day_plus_1['main']['temp_max']).split('.')[0]
    # Converting First Day max temp to celisus 
    convert_to_celisus_day1_max = int(tomorrow_min_temp); day1_calculations_max = (convert_to_celisus_day1_max - 32) * 5/9
    day1_max_metric = str(day1_calculations_max).split('.')[0]
    # Getting Tomorrows weather description
    tomorrow_weather = str(current_day_plus_1['weather'][0]['description'])

        
    
    # Two days from current dates forcast
    current_day_plus_2 = response['list'][11]
    # Day 2 Min Temp
    day2_min_temp = str(current_day_plus_2['main']['temp_min']).split('.')[0]
    # Converting Second Day min temp to celisus 
    convert_to_celisus_day2 = int(day2_min_temp); day2_calculations = (convert_to_celisus_day2 - 32) * 5/9
    day2_min_metric = str(day2_calculations).split('.')[0]
    # Day 2 Max Temp
    day2_max_temp = str(current_day_plus_2['main']['temp_max']).split('.')[0]
    # Converting Second Day max temp to celisus 
    convert_to_celisus_day2_max = int(day2_max_temp); day2_calculations_max = (convert_to_celisus_day2_max - 32) * 5/9
    day2_max_metric = str(day2_calculations_max).split('.')[0]
    # Getting Day 2 weather description
    day2_weather = str(current_day_plus_2['weather'][0]['description'])
    
    
    
    
    # Three days from current dates forcast
    current_day_plus_3 = response['list'][19]
    # Day 3 Min Temp
    day3_min_temp = str(current_day_plus_3['main']['temp_min']).split('.')[0]
    # Converting Third Day min temp to celisus 
    convert_to_celisus_day3 = int(day3_min_temp); day3_calculations = (convert_to_celisus_day3 - 32) * 5/9
    day3_min_metric = str(day3_calculations).split('.')[0]
    # Day 3 Max Temp
    day3_max_temp = str(current_day_plus_3['main']['temp_max']).split('.')[0]
    # Converting Second Day max temp to celisus 
    convert_to_celisus_day3_max = int(day3_max_temp); day3_calculations_max = (convert_to_celisus_day3_max - 32) * 5/9
    day3_max_metric = str(day3_calculations_max).split('.')[0]
    # Getting Day 3 weather description
    day3_weather = str(current_day_plus_3['weather'][0]['description'])
    
    
    # Four days from current dates forcast
    current_day_plus_4 = response['list'][27]
    # Day 4 min temp
    day4_min_temp = str(current_day_plus_4['main']['temp_min']).split('.')[0]
    # Converting Third Day min temp to celisus 
    convert_to_celisus_day4 = int(day4_min_temp); day4_calculations = (convert_to_celisus_day4 - 32) * 5/9
    day4_min_metric = str(day4_calculations).split('.')[0]
    # Day 4 max temp
    day4_max_temp = str(current_day_plus_4['main']['temp_max']).split('.')[0]
    # Converting Second Day max temp to celisus 
    convert_to_celisus_day4_max = int(day4_max_temp); day4_calculations_max = (convert_to_celisus_day4_max - 32) * 5/9
    day4_max_metric = str(day4_calculations_max).split('.')[0]
    # Getting Day 4 weather decription
    day4_weather = str(current_day_plus_4['weather'][0]['description'])
    
    

    return {
        "day1": [tomorrow_weather, tomorrow_max_temp, tomorrow_min_temp, day1_min_metric, day1_max_metric],
        "day2": [day2_weather, day2_max_temp, day2_min_temp, day2_min_metric, day2_max_metric],
        "day3": [day3_weather, day3_max_temp, day3_min_temp, day3_min_metric, day3_max_metric],
        "day4": [day4_weather, day4_max_temp, day4_min_temp, day4_min_metric, day4_max_metric],
        }
    



def metric_button():
    k = 1
    page_title = "Weather Page"
    return redirect('home', {"k": k, "page_title" : page_title})
        

def imperial_button(request):
    value = request.POST.get('imperial')
    
    k = value
    return redirect('home', {'k':k})



def shuffle_live_cameras():
    """Simple shuffle function that has the names of the places of live feeds and shuffles them so whenever
    the user refreshes the home page, the order of the live feeds will be shuffled

    Returns:
        list: the shuffled list
    """
    
    live_title = ["Dallas, TX", "Tampa, FL", "Venice Beach, CA", "Leavenworth, WA", "Brooklyn Bridge, NY"]
    
    random.shuffle(live_title)
    
    return live_title
    
    
    
    
    
def convert_time(city):
    epoch_time = int(time.time())
    # Set the API endpoint and your GeoNames username
    endpoint = "http://api.geonames.org/search"
    username = "cejkirk"
    cap_city = city
    # Set the parameters for the API request
    params = {
        "name": cap_city,
        "maxRows": 1,
        "username": username,
        "type": "json"
    }
    # Send the request to the API endpoint
    response = requests.get(endpoint, params=params)
    # Get the JSON data from the response
    data = response.json()
    # Get the continent from the JSON data
    country_code = str(data["geonames"][0]["countryCode"])
    
    # strings I have to define with '' values
    formatted_time = ''
    get_region = ''
    is_aussie = None
    day_of_the_week = ''
    spilt_region = ''
        
    try:
        if country_code == "US" and cap_city in codes.us_cities.keys():
            is_aussie = False
            # capitalize the first letter of each word in the string; example "new york" -> "New York"
            new_city = str(city).title()
            # getting the region of the US city; example "US/Eastern"
            get_region = codes.us_cities[new_city]
            # getting the current time of the server running app
            server_time = datetime.datetime.fromtimestamp(epoch_time)
            # Get the time zone for your location (US)
            local_tz = pytz.timezone(str(get_region))

            # Convert the server's local time to your local time
            local_time2 = server_time.astimezone(local_tz)
            convert_local_time2_str = str(local_time2)
            time_con2 = datetime.datetime.strptime(convert_local_time2_str, "%Y-%m-%d %H:%M:%S%z")
            day_of_the_week = time_con2.strftime("%A")
            formatted_time = time_con2.strftime("%I:%M%p")
            # 2022-12-31 18:46:41-05:00'
            region = codes.us_cities[str(city).title()]
            
            
        elif country_code != "US" and cap_city in codes.euro_cities.keys():
            if cap_city in codes.uk_cities: # Checking for UK
                is_aussie = False
                new_city = str(city).title()
                get_region = codes.euro_cities[new_city]
                server_time = datetime.datetime.fromtimestamp(epoch_time)
                tz = pytz.timezone(get_region)
                local_time2 = server_time.astimezone(tz)
                convert_local_time2_str = str(local_time2)
                time_con2 = datetime.datetime.strptime(convert_local_time2_str, "%Y-%m-%d %H:%M:%S%z")
                day_of_the_week = time_con2.strftime("%A")
                formatted_time = time_con2.strftime("%I:%M%p")
                region = codes.euro_euro_cities[str(city).title()]
                spilt_region = codes.euro_euro_cities[str(cap_city)]
                
            elif cap_city in codes.fr_cities: # Checking for France
                is_aussie = False
                # capitalize the first letter of each word in the string; example "new york" -> "New York"
                new_city = cap_city
                
                # getting the region of the city -> 'Europe/Paris'
                get_region = codes.euro_cities[new_city]

                # getting the current time of the server running app -> PythonAnywhere servers based in UK
                server_time = datetime.datetime.fromtimestamp(epoch_time)

                # # Get the time zone for the city
                tz = pytz.timezone(get_region)

                # Convert server_time to the time in the timezone represented by tz
                local_time2 = server_time.astimezone(tz)

                # Convert local_time2 to a string
                convert_local_time2_str = str(local_time2)

                # Parse the string back into a datetime object
                time_con2 = datetime.datetime.strptime(convert_local_time2_str, "%Y-%m-%d %H:%M:%S%z")

                # Format time_con2 as the full name of the day of the week
                day_of_the_week = time_con2.strftime("%A")

                # Format time_con2 as the hour and minute in 12-hour format followed by AM or PM
                formatted_time = time_con2.strftime("%I:%M%p")

                region = codes.euro_cities[str(city)]
                spilt_region = codes.euro_euro_cities[str(cap_city)]
            
            else:
                is_aussie = False
                # capitalize the first letter of each word in the string; example "new york" -> "New York"
                new_city = cap_city
                # getting the region of the city -> 'Europe/Paris'
                get_region = codes.euro_cities[new_city]
                # getting the current time of the server running app -> PythonAnywhere servers based in UK
                server_time = datetime.datetime.fromtimestamp(epoch_time)
                # # Get the time zone for the city
                tz = pytz.timezone(get_region)
                
                local_time2 = server_time.astimezone(tz)
                convert_local_time2_str = str(local_time2)
                time_con2 = datetime.datetime.strptime(convert_local_time2_str, "%Y-%m-%d %H:%M:%S%z")
                day_of_the_week = time_con2.strftime("%A")
                formatted_time = time_con2.strftime("%I:%M%p")
                region = codes.euro_cities[str(city)] 
                spilt_region = codes.euro_euro_cities[str(cap_city)] 
                    
        elif country_code != "US" and cap_city in codes.aus_cities.keys():
            is_aussie = True
            new_city = str(city).title()
            # getting the region of the US city
            get_region = codes.aus_cities[new_city]
            # getting the current time of the server running the app
            server_time = datetime.datetime.fromtimestamp(epoch_time)
            # Get the time zone for the region AU
            local_tz = pytz.timezone(str(get_region))

            # Convert the server's local time to your local time
            local_time2 = server_time.astimezone(local_tz)
            convert_local_time2_str = str(local_time2)
            time_con2 = datetime.datetime.strptime(convert_local_time2_str, "%Y-%m-%d %H:%M:%S%z")
            day_of_the_week = time_con2.strftime("%A")
            formatted_time = time_con2.strftime("%I:%M%p")
            region = codes.aus_cities[str(city).title()]

            
            
        if formatted_time[0] == "0":
            formatted_time = formatted_time[1:]
            
    except:
        return cap_city, country_code, new_city

    
    return formatted_time, is_aussie, region, day_of_the_week, spilt_region


  



def get_time_of_day(city_name):
    NOW, is_aussie, country_region, dayName, split_region = convert_time(city_name)
    currentDateAndTime = datetime.datetime.now()
    datetime_convert = str(datetime.datetime.strftime(currentDateAndTime, "%I:%p:%A")).split(":")
    hour = ''
    now_convert = NOW.split(':')
    hour1, ampm2 = now_convert
    
    ampm = ampm2[2:] # thing to return
    
    if len(hour1) == 2:
        hour = hour1
    else:
        hour = "0" + hour1
    
    
    day_ampm = hour + ampm

    
    day_cycle_list = ['06AM', '07AM', '08AM', '09AM', '10AM', '11AM', '12PM', '01PM', '02PM', '03PM', '04PM', '05PM']
    night_cycle_list = ['06PM', '07PM', '08PM', '09PM', '10PM', '11PM', '12AM', '01AM', '02AM', '03AM', '04AM', '05AM']
    
    morning_cycle = ['05AM','06AM', '07AM', '08AM', '09AM', '10AM', '11AM']
    afternoon_cycle = ['12PM', '01PM', '02PM', '03PM', '04PM']
    evening_cycle = ['04PM', '05PM', '06PM', '07PM']
    night_cycle = [ '08PM', '09PM', '10PM', '11PM', '12AM', '01AM', '02AM', '03AM', '04AM']
    
    day = None
    
    
    if day_ampm in day_cycle_list:
        day = True
    elif day_ampm in night_cycle_list:
        day = False
        
    dayTime = ''
    if day_ampm in morning_cycle:
        dayTime = 'Morning'
    elif day_ampm in afternoon_cycle:
        dayTime = 'Afternoon'
    elif day_ampm in evening_cycle:
        dayTime = 'Evening'
    elif day_ampm in night_cycle:
        dayTime = 'Night'
        

        
    
    return dayName, dayTime, day


# URL function routes



def home(request, location="arlington"):
    # Section for LIVE CAMERAS 
    LF1, LF2, LF3, LF4, LF5 = shuffle_live_cameras()
    
    
    # CURRENT DAY weather api call
    
    # Current Day Main Weather Report
    (weather_report, weather_description, current_temp, min_temp, max_temp, humidity, wind_speed,
        compass_dir, lon, lat, visual_in_miles, visual_in_kilo, city_name, metric_current_temp, metric_min_temp,
         metric_max_temp, wind_speed_metric, current_temp_length, nn) = ['Mist', 'mist', '43', '41', '45', '91%', '6', 'NNE', '-97.10', '32.73', '3', '4', 'Arlington', '6', '5', '7', '9', '2', 'None']
    
    
    cc_lon = lon # longitude of the current city
    cc_lat = lat # latitude of the current city
    
    
    # API call for the ~FIRST HOUR~ side weather widget
    (first_hour_month, first_hour_day, first_hour_time, first_hour_max, 
         first_hour_min, first_hour_description, metric_first_hour_min, metric_first_hour_max) = ("12", "20", "3:01:pm", "101", "91", "clear sky", "01", "01")
    
    # API call for the ~SECOND HOUR~ side weather widget
    (second_hour_month, second_hour_day, second_hour_time, second_hour_max, 
         second_hour_min, second_hour_description, metric_second_hour_min, metric_second_hour_max) = ("12", "20", "6:01:pm", "102", "92", "clear sky", "02", "02")
    
    # API call for the ~THIRD HOUR~ side weather widget
    (third_hour_month, third_hour_day, third_hour_time, third_hour_max, 
         third_hour_min, third_hour_description, metric_third_hour_min, metric_third_hour_max) = ("12", "20", "9:01:pm", "103", "93", "clear sky", "03", "03")
    




    # API call for the FIRST weekly forecast DAY
    # (weekly_d1_des, weekly_d1_max, weekly_d1_min, weekly_d1_metric_min, weekly_d1_metric_max) = coming_days(cc_lat, cc_lon)['day1']
    (weekly_d1_des, weekly_d1_max, weekly_d1_min, weekly_d1_metric_min, weekly_d1_metric_max)  = ('clear sky', '101', '91', '-9', '-8')

    
    # API call for the SECOND weekly forecast DAY
    # (weekly_d2_des, weekly_d2_max, weekly_d2_min, weekly_d2_metric_min, weekly_d2_metric_max) = coming_days(cc_lat, cc_lon)['day2']
    (weekly_d2_des, weekly_d2_max, weekly_d2_min, weekly_d2_metric_min, weekly_d2_metric_max) = ('light rain', '102', '92', '2', '2')

    
    # API call for the THIRD weekly forecast DAY
    # (weekly_d3_des, weekly_d3_max, weekly_d3_min, weekly_d3_metric_min, weekly_d3_metric_max) = coming_days(cc_lat, cc_lon)['day3']
    (weekly_d3_des, weekly_d3_max, weekly_d3_min, weekly_d3_metric_min, weekly_d3_metric_max) = ('thunderstorm', '103', '93', '-11', '-1')
    
    
    # API call for the FOURTH weekly forecast DAY
    # (weekly_d4_des, weekly_d4_max, weekly_d4_min, weekly_d4_metric_min, weekly_d4_metric_max) = coming_days(cc_lat, cc_lon)['day4']
    (weekly_d4_des, weekly_d4_max, weekly_d4_min, weekly_d4_metric_min, weekly_d4_metric_max)  = ('light rain', '104', '94', '-7', '4')
    
    
    
    # Checking to see if user has requested either imperial or metric values
    units_value = '0'
    imperial_value = request.POST.get('imperial')
    metric_value = request.POST.get('metric')
    
    if metric_value == '0':
        units_value = '1'
    elif metric_value == '1':
        units_value = '0'
        
    # Checking to see if user has enter their email
    submitted = False
    if request.method == "POST":
        form = SubListForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your email was saved successully')
            return HttpResponseRedirect("/home?submitted=True")
    else:
        form = SubListForm()
        if 'submitted' in request.GET:
            submitted = True
            
            
    now = datetime.datetime.now()
    NOW, is_aussie, region, day_name, split_region = convert_time(city_name)
    now = datetime.datetime.now()
    final = ''
    
    

    current_server_time = datetime.datetime.now()
    texas_tz = pytz.timezone('US/Eastern')
    convert_current_server_time_2_texas = str(current_server_time.astimezone(texas_tz))
    us_date = str(convert_current_server_time_2_texas).split(' ')[0] 
    dateDate = datetime.datetime.strptime(us_date, "%Y-%m-%d")
    formatted_date = str(dateDate.strftime("%A: %b. %d, %Y"))
    final = formatted_date + " " + NOW


    current_year = now.year
    current_day = now.day
    current_month = now.month
    current_weekday = now.weekday()
    
    
    # time_of_day = get_time_of_day(city_name)[0] # Day of the week
    # timesOfDay = get_time_of_day(city_name)[1] # Morning/Evening
    # day_time = get_time_of_day(city_name)[2] # False/True
    
    
    time_of_day, timesOfDay, day_time = get_time_of_day(city_name)
    
    days_ahead = get_next_day(time_of_day)
    d1, d2, d3, d4, d5, d6 = days_ahead
    
    


    day1 = None
    if day_time == True:
        day1 = True
    else:
        day1 = False

    weekdays = {
        0 : 'Monday', 
        1 : 'Tuesday', 
        2 : 'Wednesday',
        3 : 'Thursday',
        4 : 'Friday',
        5 : 'Saturday',
        6 : 'Sunday'
        }
    
    form = SubListForm   
    city_name = city_name + f", {region.split('/')[0]}" 
    return render(request, 'home.html', {
        "current_year": current_year,
        "form": form,
        "submitted": submitted,
        "now" : now,
        "NOW" : final,
        
        # Current Day Weather Variables
        "length_cw": current_temp_length,
        "day_of_the_week": weekdays[current_weekday],
        "current_weather": current_temp,
        "unit_value": units_value,
        "weather_main_report":weather_report,
        "city_name" : city_name,
        "weather_description" : weather_description,
        "min_temp" : min_temp,
        "visual" : visual_in_miles,
        "max_temp" : max_temp,
        "humidity" : humidity,
        "wind_speed" : wind_speed,
        "wind_dir" : compass_dir,
        "to_celsius": metric_current_temp,
        "met_min_temp" : metric_min_temp,
        "met_max_temp" : metric_max_temp,
        "met_windSpeed" : wind_speed_metric,
        "met_visual" : visual_in_kilo,
        
        # first side hour variables
        "side_forecast_month": first_hour_month,
        "side_forecast_day": first_hour_day,
        "first_hour_time": first_hour_time,
        "first_hour_description": first_hour_description,
        "first_hour_d" : first_hour_description,
        "first_hour_max": first_hour_max,
        "first_hour_min": first_hour_min,
        "metric_first_hour_max": metric_first_hour_max,
        "metric_first_hour_min": metric_first_hour_min,

        # second side hour variables
        "second_hour_max" : second_hour_max,
        "second_hour_min" : second_hour_min,
        "second_hour_month" : second_hour_month,
        "second_hour_day": second_hour_day,
        "second_hour_description" : second_hour_description,
        "second_hour_d" : second_hour_description,
        "second_hour_time" : second_hour_time,
        "metric_second_hour_max" : metric_second_hour_max,
        "metric_second_hour_min" : metric_second_hour_min,
        
        # third side hour variables
        "third_hour_max" : third_hour_max,
        "third_hour_min" : third_hour_min,
        "third_hour_month" : third_hour_month,
        "third_hour_day" : third_hour_day,
        "third_hour_time" : third_hour_time,
        "third_hour_description" : third_hour_description,
        "third_hour_d" : third_hour_description,
        "metric_third_hour_max" : metric_third_hour_max,
        "metric_third_hour_min" : metric_third_hour_min,
        
        
        # weekly forecast day 1 variables
        "weekly_description_d1" : weekly_d1_des,
        "weekly_d1_max_temp" : weekly_d1_max,
        "weekly_d1_min_temp" : weekly_d1_min,
        "weekly_d1_metric_max" : weekly_d1_metric_max,
        "weekly_d1_metric_min" : weekly_d1_metric_min,
        
        
        # weekly forecast day 2 variables
        "weekly_description_d2" : weekly_d2_des,
        "weekly_d2_max_temp" : weekly_d2_max,
        "weekly_d2_min_temp" : weekly_d2_min,
        "weekly_d2_metric_max" : weekly_d2_metric_max,
        "weekly_d2_metric_min" : weekly_d2_metric_min,
        
        
        # weekly forecast day 3 variables
        "weekly_description_d3" : weekly_d3_des,
        "weekly_d3_max_temp" : weekly_d3_max,
        "weekly_d3_min_temp" : weekly_d3_min,
        "weekly_d3_metric_max" : weekly_d3_metric_max,
        "weekly_d3_metric_min" : weekly_d3_metric_min,
        
        
        # weekly forecast day 4 variables
        "weekly_description_d4" : weekly_d4_des,
        "weekly_d4_max_temp" : weekly_d4_max,
        "weekly_d4_min_temp" : weekly_d4_min,
        "weekly_d4_metric_max" : weekly_d4_metric_max,
        "weekly_d4_metric_min" : weekly_d4_metric_min,
        
        
        
        "time_of_day" : day1,
        "time_of_day2" : timesOfDay, # variable for good 'moring' on home page
        "next_day_one" : d1,
        "next_day_two" : d2,
        "next_day_three" : d3,
        "next_day_four" : d4,
        
        
        # live camera variables
        "lf1" : LF1,
        "lf2" : LF2,
        "lf3" : LF3,
        "lf4" : LF4,
        "lf5" : LF5,
    })








def searched(request):
    searched = str(request.POST["searched-location"])

    
    if request.method == "POST":
        if ' ' in searched:
            new_search = searched.replace(" ", "%20")
        else:
            new_search = searched
        
        # Section for LIVE CAMERAS 
        LF1, LF2, LF3, LF4, LF5 = shuffle_live_cameras()
        
        
        # CURRENT DAY weather api call
        
        # Current Day Main Weather Report
        (weather_report, weather_description, current_temp, min_temp, max_temp, humidity, wind_speed,
            compass_dir, lon, lat, visual_in_miles, visual_in_kilo, city_name, metric_current_temp, metric_min_temp,
            metric_max_temp, wind_speed_metric, current_temp_length, nn,) = get_current_day_weather(new_search) #['Mist', 'mist', '43', '41', '45', '91%', '6', 'NNE', '-97.10', '32.73', '3', '4', 'Arlington', '6', '5', '7', '9', '2']
        
        
        cc_lon = lon # longitude of the current city
        cc_lat = lat # latitude of the current city
        percent_humidity = str(humidity) + "%"
        
        
        # API call for the ~FIRST HOUR~ side weather widget
        (first_hour_month, first_hour_day, first_hour_time, first_hour_max, 
            first_hour_min, first_hour_description, metric_first_hour_min, metric_first_hour_max) = ("12", "20", "3:01:pm", "101", "91", "clear sky", "01", "01")
        
        # API call for the ~SECOND HOUR~ side weather widget
        (second_hour_month, second_hour_day, second_hour_time, second_hour_max, 
            second_hour_min, second_hour_description, metric_second_hour_min, metric_second_hour_max) = ("12", "20", "6:01:pm", "102", "92", "clear sky", "02", "02")
        
        # API call for the ~THIRD HOUR~ side weather widget
        (third_hour_month, third_hour_day, third_hour_time, third_hour_max, 
            third_hour_min, third_hour_description, metric_third_hour_min, metric_third_hour_max) = ("12", "20", "9:01:pm", "103", "93", "clear sky", "03", "03")
        




        # API call for the FIRST weekly forecast DAY
        # (weekly_d1_des, weekly_d1_max, weekly_d1_min, weekly_d1_metric_min, weekly_d1_metric_max) = coming_days(cc_lat, cc_lon)['day1']
        (weekly_d1_des, weekly_d1_max, weekly_d1_min, weekly_d1_metric_min, weekly_d1_metric_max)  = ('clear sky', '101', '91', '-9', '-8')

        
        # API call for the SECOND weekly forecast DAY
        # (weekly_d2_des, weekly_d2_max, weekly_d2_min, weekly_d2_metric_min, weekly_d2_metric_max) = coming_days(cc_lat, cc_lon)['day2']
        (weekly_d2_des, weekly_d2_max, weekly_d2_min, weekly_d2_metric_min, weekly_d2_metric_max) = ('light rain', '102', '92', '2', '2')

        
        # API call for the THIRD weekly forecast DAY
        # (weekly_d3_des, weekly_d3_max, weekly_d3_min, weekly_d3_metric_min, weekly_d3_metric_max) = coming_days(cc_lat, cc_lon)['day3']
        (weekly_d3_des, weekly_d3_max, weekly_d3_min, weekly_d3_metric_min, weekly_d3_metric_max) = ('thunderstorm', '103', '93', '-11', '-1')
        
        
        # API call for the FOURTH weekly forecast DAY
        # (weekly_d4_des, weekly_d4_max, weekly_d4_min, weekly_d4_metric_min, weekly_d4_metric_max) = coming_days(cc_lat, cc_lon)['day4']
        (weekly_d4_des, weekly_d4_max, weekly_d4_min, weekly_d4_metric_min, weekly_d4_metric_max)  = ('light rain', '104', '94', '-7', '4')
        
        
        
        # Checking to see if user has requested either imperial or metric values
        units_value = '0'
        imperial_value = request.POST.get('imperial')
        metric_value = request.POST.get('metric')
        
        if metric_value == '0':
            units_value = '1'
        elif metric_value == '1':
            units_value = '0'
            
        # Checking to see if user has enter their email
        submitted = False
        if request.method == "POST":
            form = SubListForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your email was saved successully')
                return render("/home?submitted=True")
        else:
            form = SubListForm()
            if 'submitted' in request.GET:
                submitted = True
        # END Checking to see if user has enter their email
                
                
        now = datetime.datetime.now()
        NOW = convert_time(city_name)
        NOW, is_aus, region, day_name, spilt_region = convert_time(city_name)
        now = datetime.datetime.now()
        final = ''


        if is_aus == True:
            current_server_time = datetime.datetime.now()
            aus_tz = pytz.timezone('Australia/Sydney')
            convert_current_server_time_2_aus = str(current_server_time.astimezone(aus_tz))
            aus_date = str(convert_current_server_time_2_aus).split(' ')[0] 
            dateDate = datetime.datetime.strptime(aus_date, "%Y-%m-%d")
            formatted_date = str(dateDate.strftime("%A: %b. %d, %Y"))
            final = formatted_date + " " + NOW
        else:
            current_server_time = datetime.datetime.now()
            current_tz = pytz.timezone(region)
            convert_current_server_time_2_texas = str(current_server_time.astimezone(current_tz))
            us_date = str(convert_current_server_time_2_texas).split(' ')[0] 
            dateDate = datetime.datetime.strptime(us_date, "%Y-%m-%d")
            formatted_date = str(dateDate.strftime("%A: %b. %d, %Y"))
            final = formatted_date + " " + NOW
            
            
            
        current_year = now.year
        current_day = now.day
        current_month = now.month
        current_weekday = now.weekday()
        
        
        time_of_day, timesOfDay, day_time = get_time_of_day(city_name)
        
        days_ahead = get_next_day(time_of_day)
        d1, d2, d3, d4, d5, d6 = days_ahead
        
        

        day1 = None
        if day_time == True:
            day1 = True
        else:
            day1 = False

        weekdays = {
            0 : 'Monday', 
            1 : 'Tuesday', 
            2 : 'Wednesday',
            3 : 'Thursday',
            4 : 'Friday',
            5 : 'Saturday',
            6 : 'Sunday'
            }
        
        form = SubListForm    
        m = nn
        # getting the city name and adding country onto it -> London, UK
        if spilt_region != '':
            city_name = city_name + f", {spilt_region.split('/')[0]}"
        else:
            city_name = city_name + f", {region.split('/')[0]}"
            
        
        return render(request, 'searched.html', {
            "none_result": nn,
            "type" : m,
            "form": form,
            "current_year": current_year,
            "submitted": submitted,
            "now" : now,
            "search_value": searched,
            "NOW": final,
            
            # Current Day Weather Variables
            "length_cw": current_temp_length,
            "day_of_the_week": weekdays[current_weekday],
            "current_weather": current_temp,
            "unit_value": units_value,
            "main_report":weather_report,
            "city_name" : city_name,
            "weather_description" : weather_description,
            "min_temp" : min_temp,
            "visual" : visual_in_miles,
            "max_temp" : max_temp,
            "humidity" : percent_humidity,
            "wind_speed" : wind_speed,
            "wind_dir" : compass_dir,
            "to_celsius": metric_current_temp,
            "met_min_temp" : metric_min_temp,
            "met_max_temp" : metric_max_temp,
            "met_windSpeed" : wind_speed_metric,
            "met_visual" : visual_in_kilo,
            
            # first side hour variables
            "side_forecast_month": first_hour_month,
            "side_forecast_day": first_hour_day,
            "first_hour_time": first_hour_time,
            "first_hour_description": first_hour_description,
            "first_hour_d" : first_hour_description,
            "first_hour_max": first_hour_max,
            "first_hour_min": first_hour_min,
            "metric_first_hour_max": metric_first_hour_max,
            "metric_first_hour_min": metric_first_hour_min,

            # second side hour variables
            "second_hour_max" : second_hour_max,
            "second_hour_min" : second_hour_min,
            "second_hour_month" : second_hour_month,
            "second_hour_day": second_hour_day,
            "second_hour_description" : second_hour_description,
            "second_hour_d" : second_hour_description,
            "second_hour_time" : second_hour_time,
            "metric_second_hour_max" : metric_second_hour_max,
            "metric_second_hour_min" : metric_second_hour_min,
            
            # third side hour variables
            "third_hour_max" : third_hour_max,
            "third_hour_min" : third_hour_min,
            "third_hour_month" : third_hour_month,
            "third_hour_day" : third_hour_day,
            "third_hour_time" : third_hour_time,
            "third_hour_description" : third_hour_description,
            "third_hour_d" : third_hour_description,
            "metric_third_hour_max" : metric_third_hour_max,
            "metric_third_hour_min" : metric_third_hour_min,
            
            
            # weekly forecast day 1 variables
            "weekly_description_d1" : weekly_d1_des,
            "weekly_d1_max_temp" : weekly_d1_max,
            "weekly_d1_min_temp" : weekly_d1_min,
            "weekly_d1_metric_max" : weekly_d1_metric_max,
            "weekly_d1_metric_min" : weekly_d1_metric_min,
            
            
            # weekly forecast day 2 variables
            "weekly_description_d2" : weekly_d2_des,
            "weekly_d2_max_temp" : weekly_d2_max,
            "weekly_d2_min_temp" : weekly_d2_min,
            "weekly_d2_metric_max" : weekly_d2_metric_max,
            "weekly_d2_metric_min" : weekly_d2_metric_min,
            
            
            # weekly forecast day 3 variables
            "weekly_description_d3" : weekly_d3_des,
            "weekly_d3_max_temp" : weekly_d3_max,
            "weekly_d3_min_temp" : weekly_d3_min,
            "weekly_d3_metric_max" : weekly_d3_metric_max,
            "weekly_d3_metric_min" : weekly_d3_metric_min,
            
            
            # weekly forecast day 4 variables
            "weekly_description_d4" : weekly_d4_des,
            "weekly_d4_max_temp" : weekly_d4_max,
            "weekly_d4_min_temp" : weekly_d4_min,
            "weekly_d4_metric_max" : weekly_d4_metric_max,
            "weekly_d4_metric_min" : weekly_d4_metric_min,
            
            
            
            "time_of_day" : day1,
            "time_of_day2" : timesOfDay, # variable for good 'moring' on home page
            "next_day_one" : d1,
            "next_day_two" : d2,
            "next_day_three" : d3,
            "next_day_four" : d4,
            
            
            # live camera variables
            "lf1" : LF1,
            "lf2" : LF2,
            "lf3" : LF3,
        })   





def about(request):
    form = SubListForm   
    
    # Checking to see if user has enter their email
    submitted = False
    if request.method == "POST":
        form = SubListForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your email was saved successully')
            return render("/home?submitted=True")
    else:
        form = SubListForm()
        if 'submitted' in request.GET:
            submitted = True
    # END Checking to see if user has enter their email
    return render(request, 'about.html', {"form":form})






def news(request):
    form = SubListForm
    # Checking to see if user has enter their email
    submitted = False
    if request.method == "POST":
        form = SubListForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your email was saved successully')
            return render("/home?submitted=True")
    else:
        form = SubListForm()
        if 'submitted' in request.GET:
            submitted = True
    # END Checking to see if user has enter their email 
    return render(request, 'news.html', {"form":form})





def live_cameras(request):
    LF1, LF2, LF3, LF4, LF5 = shuffle_live_cameras()
    form = SubListForm   
    
    
    # Checking to see if user has enter their email
    submitted = False
    if request.method == "POST":
        form = SubListForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your email was saved successully')
            return render("/home?submitted=True")
    else:
        form = SubListForm()
        if 'submitted' in request.GET:
            submitted = True
    # END Checking to see if user has enter their email
    
    
    return render(request, 'live_cameras.html', {
        "form":form,
        # live camera variables
        "lf1" : LF1,
        "lf2" : LF2,
        "lf3" : LF3,
        })
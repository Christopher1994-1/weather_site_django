from django.test import TestCase
from datetime import *
import random
from datetime import datetime
from calendar import *
import datetime
import pytz
from os import environ
import requests
import time
import codes
import json
import sqlite3

# Create your tests here.

def check_shit(city):
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
    
    
    return cap_city, country_code, data




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
        try:
            return cap_city, country_code, new_city
        except:
            a, b, c = check_shit(cap_city)
            return a, b, c


    
    return formatted_time, is_aussie, region, day_of_the_week, spilt_region





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
        
    



city = "Esbjerg"

(weather_report, weather_description, current_temp, min_temp, max_temp, humidity, wind_speed,
    compass_dir, lon, lat, visual_in_miles, visual_in_kilo, city_name, metric_current_temp, metric_min_temp,
    metric_max_temp, wind_speed_metric, current_temp_length, nn,) = get_current_day_weather(city)

try:
    a, b, c, d, e = convert_time(city_name)

    print(f" city name from get_current_day_weather() - '{city_name}'")
    print(f" variable 'formatted_time' value returned: - '{a}'")
    print(f" variable 'is_aussie' value returned: - '{b}'")
    print(f" variable 'region' value returned: - '{c}'")
    print(f" variable 'day_of_the_week' value returned: - '{d}'")
    print(f" variable 'spilt_region' value returned: - '{e}'")

    print("=" * 20)

    print(f"Main Weather report for {city_name} is {weather_report}, it is {current_temp} and {humidity}% humidity")
except:
    try:
        a, b, c = convert_time(city_name)
        print(f"Error Happened: cap_city variable '{a}'")
        print(f"Error Happened: country_code variable '{b}'")
        print(f"Error Happened: new_city variable '{b}'")
    except:
        a, b, c = convert_time(city_name)
        print(a)
        print(b)
        print()
        print(c)
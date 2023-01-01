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
from codes import all_cities
import json

# Create your tests here.

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
    




def compass_directions(direction):
    directions = {"North":"N",
                  "North North East":"NNE",
                  "North East":"North East",
                  "East North East":"ENE",
                  "East":"E",
                  "East South East":"ESE",
                  "South East":"SE",
                  "South South East":"SE",
                  "South":"S",
                  "South South West":"SSW",
                  "South West":"SW",
                  "West South West":"WSW",
                  "West":"W",
                  "West North West":"WNW",
                  "North West":"NW",
                  "North North West":"NNW"
                  }
    new_direction = ''
    if direction in directions.keys():
        new_direction = directions[direction]
        
    return new_direction





def get_next_day():
    """Returns a list of the next five weekdays after the current day.
    
    Returns:
        list: A list of strings representing the next five weekdays. The list
              will start with the current day and end with the fourth day after
              the current day. For example, if it is currently Wednesday, the
              returned list will be ['Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].
    """
    
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
            response1_prettyprint = json.dumps(response1, indent=3)
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
          return [get_main, get_weather_des, current_temp_str, min_temp_str, max_temp_str, humidity, wind_speed,
                     CompassDir, LON, LAT, visual_in_miles, visual_in_kilo, city_name, metric_current_temp,
                   metric_min_temp, metric_max_temp, wind_speed_metric, current_temp_length, search_result_false]
    except UnboundLocalError:
        return "None"
        



def convert_time(city):
    epoch_time = int(time.time())
    # Set the API endpoint and your GeoNames username
    endpoint = "http://api.geonames.org/search"
    username = "cejkirk"
    # Set the parameters for the API request
    params = {
        "name": str(city),
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
    region = all_cities[city_name.title()]
    
    # strings I have to define with '' values
    formatted_time = ''
    get_region = ''
    
    if country_code == "US":
        is_aussie = False
        # capitalize the first letter of each word in the string; example "new york" -> "New York"
        new_city = str(city).title()
        # getting the region of the US city; example "US/Eastern"
        get_region = all_cities[new_city]
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
        
        
    elif country_code != "US":
        if country_code in all_cities.keys():
            is_aussie = False
            # capitalize the first letter of each word in the string; example "new york" -> "New York"
            new_city = str(city).title()
            # getting the region of the US city
            get_region = all_cities[new_city]
            # getting the current time of the server running app
            server_time = datetime.datetime.fromtimestamp(epoch_time)
            # # Get the time zone for the city
            tz = pytz.timezone(get_region)
            # # Convert the server time to the local time for the city
            local_time = str(server_time.astimezone(tz)).split(' ')[1]
            time_con = datetime.datetime.strptime(local_time, "%H:%M:%S%z")
            # # Format the time as a string
            formatted_time = time_con.strftime("%I:%M%p")
            
        elif country_code == "AU":
            is_aussie = True
            new_city = str(city).title()
            # getting the region of the US city
            get_region = all_cities[new_city]
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
            
    if formatted_time[0] == "0":
        formatted_time = formatted_time[1:]

    
    return formatted_time, is_aussie, region, day_of_the_week
    




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
    
















# function to call to determine night or day
def get_time_of_day(city_name):
    NOW, is_aussie, country_region, dayName = convert_time(city_name)
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





city_name = "sydney"
NOW, is_aussie, country_region, day_name = convert_time(city_name)
now = datetime.datetime.now()
final = ''

if is_aussie == True:
    current_server_time = datetime.datetime.now()
    aus_tz = pytz.timezone('Australia/Sydney')
    convert_current_server_time_2_aus = str(current_server_time.astimezone(aus_tz))
    aus_date = str(convert_current_server_time_2_aus).split(' ')[0] 
    dateDate = datetime.datetime.strptime(aus_date, "%Y-%m-%d")
    formatted_date = str(dateDate.strftime("%A: %b. %d, %Y"))
    final = formatted_date + " " + NOW
    
    
else:
    current_server_time = datetime.datetime.now()
    current_tz = pytz.timezone(country_region)
    convert_current_server_time_2_texas = str(current_server_time.astimezone(current_tz))
    us_date = str(convert_current_server_time_2_texas).split(' ')[0] 
    dateDate = datetime.datetime.strptime(us_date, "%Y-%m-%d")
    formatted_date = str(dateDate.strftime("%A: %b. %d, %Y"))
    final = formatted_date + " " + NOW


a, b, c, d = convert_time(city_name)

print("Variables returning from the function convert_time")
print(a)
print(b)
print(c)
print(d)


print()



a2, b2, c2, = get_time_of_day(city_name)


print("Variables returning from the function get_time_of_day")
print(a2)
print(b2)
print(c2)

















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
    


def shuffle_live_cameras():
    """Simple shuffle function that has the names of the places of live feeds and shuffles them so whenever
    the user refreshes the home page, the order of the live feeds will be shuffled

    Returns:
        list: the shuffled list
    """
    
    live_title = ["Dallas, TX", "Tampa, FL", "Venice Beach, CA", "Leavenworth, WA", "Brooklyn Bridge, NY"]
    
    random.shuffle(live_title)
    
    return live_title
    





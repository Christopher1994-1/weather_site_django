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


def convertt_time(city):
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

    region = "GB/Europe"#codes.all_cities[str(city).title()]

    # strings I have to define with '' values
    formatted_time = ''
    get_region = ''
    uk = ''
    is_aussie = None
    day_of_the_week = ''
    
    if country_code == "US":
        is_aussie = False
        # capitalize the first letter of each word in the string; example "new york" -> "New York"
        new_city = str(city).title()
        # getting the region of the US city; example "US/Eastern"
        get_region = codes.all_cities[new_city]
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
        
        # we are getting a error that does not show the time for GB, when the user types in 'lodnon'
        
    elif country_code != "US":
        if country_code in codes.all_cities.keys():
            is_aussie = False
            # capitalize the first letter of each word in the string; example "new york" -> "New York"
            new_city = str(city).title()
            # getting the region of the US city
            get_region = codes.all_cities[new_city]
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
            get_region = codes.all_cities[new_city]
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

    
         
    # if formatted_time[0] == "0":
    #     formatted_time = formatted_time[1:]

    
    return formatted_time, is_aussie, region, day_of_the_week
    

        


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
    region = codes.all_cities[str(city).title()]
    
    # strings I have to define with '' values
    formatted_time = ''
    get_region = ''
    
    if country_code == "US":
        is_aussie = False
        # capitalize the first letter of each word in the string; example "new york" -> "New York"
        new_city = str(city).title()
        # getting the region of the US city; example "US/Eastern"
        get_region = codes.all_cities[new_city]
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
        if country_code in codes.all_cities.keys():
            is_aussie = False
            # capitalize the first letter of each word in the string; example "new york" -> "New York"
            new_city = str(city).title()
            # getting the region of the US city
            get_region = codes.all_cities[new_city]
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
            get_region = codes.all_cities[new_city]
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
city_name = "london"



NOW, is_aussie, region, day_name = convert_time(city_name)


city_name = city_name + f", {region.split('/')[0]}"

print(NOW)



# this is the error we get for running the code above, figure it out


#     if formatted_time[0] == "0":
#        ~~~~~~~~~~~~~~^^^
# IndexError: string index out of range

from django.test import TestCase
from datetime import *
from calendar import *
from os import environ
import requests

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

print(next5days)

# next_day1 = next5days[0]
# next_day2 = next5days[1]
# next_day3 = next5days[2]
# next_day4 = next5days[3]
# next_day5 = next5days[4]

# print(next_day1, next_day2, next_day3, next_day4, next_day5)


BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = environ.get("CEJ_Weather_API")
CITY = "Arlington"

url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY

response = requests.get(url).json()

print(response)
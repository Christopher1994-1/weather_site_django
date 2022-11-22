from django.test import TestCase
from datetime import *
from calendar import *

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

next_day1 = next5days[0]
next_day2 = next5days[1]
next_day3 = next5days[2]
next_day4 = next5days[3]
next_day5 = next5days[4]

print(next_day1, next_day2, next_day3, next_day4, next_day5)

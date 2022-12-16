from django.test import TestCase
from datetime import *
import random
from datetime import datetime
from calendar import *
import datetime
from os import environ
import requests
import time
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
    
    try:
        get_main = response1["weather"][0]["main"]
        get_weather_des = response1["weather"][0]["description"] # clear sky
        current_temp = response1["main"]['temp'] # current temperature
        min_temp = response1["main"]["temp_min"] # temperature low
        max_temp = response1["main"]["temp_max"] # temperature high
        humidity = response1["main"]["humidity"] # humidity
        wind_speed = str(response1["wind"]["speed"]).split(".")[0] # wind speed
        wind_direction = int(response1["wind"]["deg"]) # wind direction in degrees, pass into calculate_wind()
        city_name = response1["name"]
        visual = response1["visibility"]
        
        
        # converting current temp to metric 
        spilt_current_temp = str(current_temp).split('.')[0]
        toInt_cw = int(spilt_current_temp)
        toInt_cw2 = (toInt_cw - 32) * 5/9
        metric_current_temp = str(toInt_cw2).split('.')[0]
        
        
        # converting min temp to metric 
        spilt_min_temp = str(min_temp).split('.')[0]
        toInt_min = int(spilt_min_temp)
        toInt_min2 = (toInt_min - 32) * 5/9
        metric_min_temp = str(toInt_min2).split('.')[0]
        
        
        # converting max temp to metric 
        spilt_max_temp = str(max_temp).split('.')[0]
        toInt_max = int(spilt_max_temp)
        toInt_max2 = (toInt_max - 32) * 5/9
        metric_max_temp = str(toInt_max2).split('.')[0]
        
        
        # converting wind speed to metric
        toIntWind = int(wind_speed) * 1.609
        wind_speed_metric = str(toIntWind).split('.')[0]
        
        
        # converting visibility to mph/k
        
        

        
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
        'none'
    
        
        
    try:
        return (get_main, get_weather_des, current_temp, min_temp, max_temp, 
                humidity, wind_speed, CompassDir, LON, LAT, visual, city_name, metric_current_temp, 
                metric_min_temp, metric_max_temp, wind_speed_metric)
    except UnboundLocalError:
        return "None"
        

j = get_current_day_weather()

print(j)


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








cc_lon = "-97.10"
cc_lat = "32.73"





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

        
    # Two days from current dates forcast
    current_day_plus_2 = response['list'][11]
    day2_min_temp = str(current_day_plus_2['main']['temp_min']).split('.')[0]
    day2_max_temp = str(current_day_plus_2['main']['temp_max']).split('.')[0]
    day2_weather = str(current_day_plus_2['weather'][0]['description'])
    
    
    # Three days from current dates forcast
    current_day_plus_3 = response['list'][19]
    day3_min_temp = str(current_day_plus_3['main']['temp_min']).split('.')[0]
    day3_max_temp = str(current_day_plus_3['main']['temp_max']).split('.')[0]
    day3_weather = str(current_day_plus_3['weather'][0]['description'])
    
    
    # Four days from current dates forcast
    current_day_plus_4 = response['list'][27]
    day4_min_temp = str(current_day_plus_4['main']['temp_min']).split('.')[0]
    day4_max_temp = str(current_day_plus_4['main']['temp_max']).split('.')[0]
    day4_weather = str(current_day_plus_4['weather'][0]['description'])
    
    
    # Five days from current dates forcast
    current_day_plus_5 = response['list'][35]
    day5_min_temp = str(current_day_plus_5['main']['temp_min']).split('.')[0]
    day5_max_temp = str(current_day_plus_5['main']['temp_max']).split('.')[0]
    day5_weather = str(current_day_plus_5['weather'][0]['description'])
    
    return {
        "day1": [tomorrow_weather, tomorrow_max_temp, tomorrow_min_temp],
        "day2": [day2_weather, day2_max_temp, day2_min_temp],
        "day3": [day3_weather, day3_max_temp, day3_min_temp],
        "day4": [day4_weather, day4_max_temp, day4_min_temp],
        "day5": [day5_weather, day5_max_temp, day5_min_temp],
        }
    

# function to call to determine night or day
def get_time_of_day():
    currentDateAndTime = datetime.datetime.now()
    datetime_convert = str(datetime.datetime.strftime(currentDateAndTime, "%I:%p:%A")).split(":")
    
    hour, ampm, day_of_the_week = datetime_convert
    
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
        

        
    
    return day, dayTime, day_of_the_week


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
    







def getting_all_info(city):
    
    now = datetime.datetime.now()
    current_weekday = now.weekday()

    days = {
        0 : "Sunday",
        1 : "Monday",
        2 : "Tuesday",
        3 : "Wednesday",
        4 : "Thursday",
        5 : "Friday",
        6 : "Saturday",
    }


    today = days[current_weekday]
    next_days = get_next_day(today)
    
    
    # Section for LIVE CAMERAS 
    LF1, LF2, LF3, LF4, LF5 = shuffle_live_cameras()
    
    
    # GETTING CURRENT WEATHER API CALLS
    current_call = get_current_day_weather(city)
    
    if current_call == "None":
        current_call = get_current_day_weather("Arlington")
        # current_call = ['Clear', 'clear sky', '37.8', '35.58', '41.56', '69', '9', 'North West', '-97.10', '32.73', '10000', 'Arlington']
        (main_weather, weather_description, current_temp, min_temp, 
        max_temp, humidity, wind_speed, compassDir, lon, lat, visual, city_name) = current_call
    else:
        current_call = get_current_day_weather(city)
        # current_call = ['Clear', 'clear sky', '37.8', '35.58', '41.56', '69', '9', 'North West', '-97.10', '32.73', '10000', 'Arlington']
        (main_weather, weather_description, current_temp, min_temp, 
        max_temp, humidity, wind_speed, compassDir, lon, lat, visual, city_name) = current_call


    # SPLITING ~CURRENT WEATHER~ FROM FLOAT TO INT
    convert_current_weather = str(current_temp).split('.')[0]
    
    
    
    # CHECKING THE LENGTH OF CURRENT TEMPERATURE 
    current_weather_length = len(convert_current_weather)
    
    
    # CONVERTING ~CURRENT TEMP~ TO METIRC
    current_temp_int = (int(convert_current_weather) - 32) * 5/9
    current_temp_metric = str(current_temp_int).split('.')[0]
    

    # CONVERTING ~MIN~ TEMPERATURE TO METRIC
    convert_min_temp = str(min_temp).split('.')[0]
    str_minTemp = (int(convert_min_temp) - 32) * 5/9
    min_temp_metric = str(str_minTemp).split('.')[0]
    
 
    # CONVERTING ~MAX~ TEMPERATURE TO METRIC 
    convert_max_temp = str(max_temp).split('.')[0]
    str_maxTemp = (int(convert_max_temp) - 32) * 5/9
    max_temp_metric = str(str_maxTemp).split('.')[0]
    
    # ADDING % TO THE END OF HUMIDITY VARIABLE
    new_humidity = str(humidity) + "%"
    
    
    # CONVERTING ~WIND SPEED~ TEMPERATURE TO METRIC
    str_windSpeed = (int(wind_speed) * 1.609)
    met_windSpeed = str(str_windSpeed).split('.')[0]
    
    
    # CONVERTING ~VISUAL TO MILES~
    convert_wind = int(visual) // 1609
    visual = str(convert_wind)
    
    str_visual = (int(visual) * 1.609)
    met_visual = str(str_visual).split('.')[0]
    
    
    # GETTING COMPASS DIRECTION 
    new_direction = compass_directions(compassDir)
    

    # API CALLS FOR THE SIDE HOURS ###########################

    # # # API call for the ~FIRST HOUR~ side weather widget
    (first_hour_month, first_hour_day, first_hour_time, 
     first_hour_max, first_hour_min, first_hour_description) = weather_next_few_hours(lat, lon)[0]
    # f_h_month, f_h_day, f_h_time, f_h_des, f_h_max, f_h_min = ("11", "30", "3:01:pm", "light rain", "101", "91")
    
    # ~FIRST HOUR~ METRIC CONVERTION FOR ~MAX HOUR~
    convert_first_hour_max = int(first_hour_max)
    f_h_max_metric = (convert_first_hour_max - 32) * 5/9
    first_hour_max_metric = str(f_h_max_metric).split('.')[0]
    
    
    # ~FIRST HOUR~ METRIC CONVERTION FOR ~MIN HOUR~
    convert_first_hour_min = int(first_hour_min)
    f_h_min_metric = (convert_first_hour_min - 32) * 5/9
    first_hour_min_metric = str(f_h_min_metric).split('.')[0]
    
    
    
    
    
    # API call for the ~SECOND HOUR~ side weather widget
    (second_hour_month, second_hour_day, second_hour_time, 
     second_hour_max, second_hour_min, second_hour_description) = weather_next_few_hours(lat, lon)[1]
    # s_h_month, s_h_day, s_h_time, s_h_des, s_h_max, s_h_min = ("11", "30", "6:00:pm", "clear sky", "102", "92")
    
    
    # ~SECOND HOUR~ METRIC CONVERTION FOR ~MIN HOUR~
    convert_second_hour_min = int(second_hour_min)
    second_hour_min_metric = (convert_second_hour_min - 32) * 5/9
    second_hour_min_metric = str(second_hour_min_metric).split('.')[0]
    
    
    # ~SECOND HOUR~ METRIC CONVERTION FOR ~MAX HOUR~
    convert_second_hour_max = int(second_hour_max)
    second_hour_max_metric = (convert_second_hour_max - 32) * 5/9
    second_hour_max_metric = str(second_hour_max_metric).split('.')[0]
    
    
    
    
    
    
    
    # API call for the ~THIRD HOUR~ side weather widget
    (third_hour_month, third_hour_day, third_hour_time, third_hour_max, 
     third_hour_min, third_hour_description) = weather_next_few_hours(lat, lon)[2]
    # t_h_month, t_h_day, t_h_time, t_h_des, t_h_max, t_h_min = ('11', '30', '9:00:pm', 'rain', '103', '93')


    # ~THIRD HOUR~ METRIC CONVERTION FOR ~MIN HOUR~
    convert_third_hour_min = int(third_hour_min)
    third_hour_min_metric = (convert_third_hour_min - 32) * 5/9
    third_hour_min_metric = str(third_hour_min_metric).split('.')[0]
    
    
    # ~THIRD HOUR~ METRIC CONVERTION FOR ~MAX HOUR~
    convert_third_hour_max = int(third_hour_max)
    third_hour_max_metric = (convert_third_hour_max - 32) * 5/9
    third_hour_max_metric = str(third_hour_max_metric).split('.')[0]





    # ##################################################################


    # # # API call for the FIRST weekly forecast DAY
    (weekly_d1_descripton, weekly_d1_max, weekly_d1_min) = coming_days(lat, lon)['day1']
    # weekly_d1_descripton, weekly_d1_max, weekly_d1_min  = ('clear sky', '101', '91', 'date', 'idk')

    # ~FIRST DAY~ METRIC CONVERTION FOR ~MIN HOUR~
    convert_first_day_min = int(weekly_d1_min)
    first_day_min = (convert_first_day_min - 32) * 5/9
    first_day_min_metric = str(first_day_min).split('.')[0]
    
    
    # ~FIRST DAY~ METRIC CONVERTION FOR ~MAX HOUR~
    convert_first_day_max = int(weekly_d1_max)
    first_day_max = (convert_first_day_max - 32) * 5/9
    first_day_max_metric = str(first_day_max).split('.')[0]
    
    
    # GETTING ~WEEKDAY~ DAY FOR ~FIRST DAY~
    first_day_weekday = next_days[0]
    
    
    
    
    
    # # # API call for the SECOND weekly forecast DAY
    (weekly_d2_desription, weekly_d2_max, weekly_d2_min)  = coming_days(lat, lon)['day2']
    # weekly_d2_des, weekly_d2_max, weekly_d2_min, weekly_d2_date, weekly_d2_day  = ('light rain', '102', '92', 'date', 'idk')

    
    # ~SECOND DAY~ METRIC CONVERTION FOR ~MIN HOUR~
    convert_second_day_min = int(weekly_d2_min)
    second_day_min = (convert_second_day_min - 32) * 5/9
    second_day_min_metric = str(second_day_min).split('.')[0]
    
    
    # ~SECOND DAY~ METRIC CONVERTION FOR ~MAX HOUR~
    convert_second_day_max = int(weekly_d2_max)
    second_day_max = (convert_second_day_max - 32) * 5/9
    second_day_max_metric = str(second_day_max).split('.')[0]
    
    
    # GETTING ~WEEKDAY~ DAY FOR ~SECOND DAY~
    second_day_weekday = next_days[1]
    
    
    
    # # # API call for the THIRD weekly forecast DAY
    # # # weekly_d3_des, weekly_d3_max, weekly_d3_min, weekly_d3_date, weekly_d3_day  = coming_days(cc_lat, cc_lon)['day3']
    # weekly_d3_des, weekly_d3_max, weekly_d3_min, weekly_d3_date, weekly_d3_day  = ('thunderstorm', '103', '93', 'date', 'idk')

    
    
    # # # API call for the FOURTH weekly forecast DAY
    # # # weekly_d4_des, weekly_d4_max, weekly_d4_min, weekly_d4_date, weekly_d4_day  = coming_days(cc_lat, cc_lon)['day4']
    # weekly_d4_des, weekly_d4_max, weekly_d4_min, weekly_d4_date, weekly_d4_day  = ('light rain', '104', '94', 'date', 'idk')
    # # for converting day one max imperial to metric 
    # weekly_d4_max_metric = (int(weekly_d4_max) - 32) * 5/9
    # weekly_d4_max_metric_str = str(weekly_d4_max_metric).split('.')[0]
    # # for converting day one max metric to imperial
    # weekly_d4_min_metric = (int(weekly_d4_min) - 32) * 5/9
    # weekly_d4_min_metric_str = str(weekly_d4_min_metric).split('.')[0]
    
    
            
    # now = datetime.datetime.now()
    # current_year = now.year
    # current_day = now.day
    # current_month = now.month
    # current_weekday = now.weekday()
    
    
    # day_time = get_time_of_day()[0] # False/True
    # time_of_day = get_time_of_day()[2] # Day of the week
    
    # days_ahead = get_next_day(time_of_day)
    # d1, d2, d3, d4, d5, d6 = days_ahead
    
    
    # timesOfDay = get_time_of_day()[1]

    # day1 = None
    # if day_time == True:
    #     day1 = True
    # else:
    #     day1 = False

    # weekdays = {
    #     0 : 'Monday', 
    #     1 : 'Tuesday', 
    #     2 : 'Wednesday',
    #     3 : 'Thursday',
    #     4 : 'Friday',
    #     5 : 'Saturday',
    #     6 : 'Sunday'
    #     }
    
    
    
    return {"main_weather" : [main_weather, weather_description, convert_current_weather, current_weather_length, current_temp_metric,
                               min_temp_metric, max_temp_metric, new_humidity, wind_speed, met_windSpeed, visual, met_visual, new_direction, city_name],
            "first_hour": [first_hour_month, first_hour_day, first_hour_time, first_hour_max, first_hour_min, first_hour_description, first_hour_max_metric, first_hour_min_metric],
            "second_hour": [second_hour_month, second_hour_day, second_hour_time, second_hour_max, second_hour_min,
                     second_hour_description, second_hour_max_metric, second_hour_min_metric],
            "third_hour": [third_hour_month, third_hour_day, third_hour_time, third_hour_max, third_hour_min,
                     third_hour_description, third_hour_max_metric, third_hour_min_metric],
            "first_day": [weekly_d1_descripton, weekly_d1_max, weekly_d1_min, first_day_min_metric, first_day_max_metric, first_day_weekday],
            "second day": [weekly_d2_desription, weekly_d2_max, weekly_d2_min, second_day_min_metric, second_day_max_metric, second_day_weekday],
            }



# city = input("> ")

# test = getting_all_info(city)

# print(f"The type Returned: {type(test)}")

# print()


# print(test)



from django.shortcuts import render, redirect
from datetime import *
from .forms import SubListForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from string import capwords
import calendar
import json
from os import environ
import requests


def get_time_of_day(time):
    if time < 12:
        return "Morning"
    elif time < 16:
        return "Afternoon"
    elif time < 19:
        return "Evening"
    else:
        return "Night"


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
        
    return next_five_days, next_day
        
        

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
    city_name = response1["name"]
    wd = response1["weather"][0]["description"]
    visual = response1["visibility"]
    
    
    sector = {
        1 : "N",
        2 : "NNE",
        3 : "NE",
        4 : "ENE",
        5 : "E",
        6 : "ESE",
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
        
    current_date = get_next_day()[1]
        
        
        
    return get_weather_report, current_temp, min_temp, max_temp, humidity, wind_speed, CompassDir, LON, LAT, current_date, city_name, wd, visual
        

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
    


def metric_button():
    k = 1
    return redirect('home', {"k": k})
        

def imperial_button(request):
    value = request.POST.get('imperial')
    
    k = value
    return redirect('home', {'k':k})



def home(request, location="arlington"):
    # weather calls 
    # current_weather = str(get_current_day_weather()[1]).split(".")[0]
    current_weather = "65"
    length_cw = len(current_weather)
    cw_int = (int(current_weather) - 32) * 5/9
    cw_int = str(cw_int).split('.')[0]
    
    # city_name = str(get_current_day_weather()[10])
    city_name = "Bonadelle Ranchos-Madera Ranchos"
    wd = "Rain"
    # weather_description = str(get_current_day_weather()[11])
    weather_description = "few clouds"
    # min_temp = str(get_current_day_weather()[2]).split(".")[0]
    min_temp = "105"
    # max_temp = str(get_current_day_weather()[3]).split(".")[0]
    max_temp = "58"
    # humidity = str(get_current_day_weather()[4]) + "%"
    humidity = "58%"
    # wind_speed = str(get_current_day_weather()[5])
    wind_speed = "105"
    # wind_dir = str(get_current_day_weather()[6])
    wind_dir = "NNW"
    # visual = str(get_current_day_weather()[12])
    visual = "10000"
    convert_wind = int(visual) // 1609
    visual = str(convert_wind)
    
    
    # cc_lon = get_current_day_weather()[7]
    cc_lon = "-97.10"
    # cc_lat = get_current_day_weather()[8]
    cc_lat = "32.73"
    # API call for the main weather widget
    # w_main, current_weather, min_temp, max_temp, humidity, wind_speed, wind_dir, cc_lon, cc_lat, current_date, city_name, wd, visual  = get_current_day_weather()[0]
    
    first_hour_d = 'light intensity shower rain'
    
    # API call for the first hour side weather widget
    f_h_month = "11"
    f_h_day = "30"
    f_h_time = "3:00"
    f_h_max = "58"
    f_h_min = "34"
    
    # f_h_month, f_h_day, f_h_time, f_h_max, f_h_min, f_h_des = weather_next_few_hours(cc_lat, cc_lon)[0]
    # API call for the second hour side weather widget
    # s_h_month, s_h_day, s_h_time, s_h_max, s_h_min, s_h_des = weather_next_few_hours(cc_lat, cc_lon)[1]
    # API call for the third hour side weather widget
    # t_h_month, t_h_day, t_h_time, t_h_max, t_h_min, t_h_des = weather_next_few_hours(cc_lat, cc_lon)[2]
    
    
    # Second Hour variables
    # side_forecast_month = weather_next_few_hours(cc_lat, cc_lon)[1][0]
    # side_forecast_day = weather_next_few_hours(cc_lat, cc_lon)[1][1]
    # second_hour_time = weather_next_few_hours(cc_lat, cc_lon)[1][2]
    # second_hour_max = weather_next_few_hours(cc_lat, cc_lon)[1][3]
    # second_hour_min = weather_next_few_hours(cc_lat, cc_lon)[1][4]
    # second_hour_d = weather_next_few_hours(cc_lat, cc_lon)[1][5]
    second_hour_d = 'thunderstorm'
    
    # Third Hour variables
    # side_forecast_month = weather_next_few_hours(cc_lat, cc_lon)[2][0]
    # side_forecast_day = weather_next_few_hours(cc_lat, cc_lon)[2][1]
    # second_hour_time = weather_next_few_hours(cc_lat, cc_lon)[2][2]
    # second_hour_max = weather_next_few_hours(cc_lat, cc_lon)[2][3]
    # second_hour_min = weather_next_few_hours(cc_lat, cc_lon)[2][4]
    # second_hour_d = weather_next_few_hours(cc_lat, cc_lon)[2][5]
    third_hour_d = 'clear sky'
    
    # next few hour calls

    
    
    
    units_value = '0'
    imperial_value = request.POST.get('imperial')
    metric_value = request.POST.get('metric')
    
    if metric_value == '0':
        units_value = '1'
    elif metric_value == '1':
        units_value = '0'
        
    
    submitted = False
    if request.method == "POST":
        form = SubListForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your email was saved successully')
            return HttpResponseRedirect('/home?submitted=True')
    else:
        form = SubListForm()
        if 'submitted' in request.GET:
            submitted = True
            
            
    now = datetime.now()
    current_year = now.year
    current_day = now.day
    current_month = now.month
    current_weekday = now.weekday()
    day = None
    time_of_day = get_time_of_day((now.hour))
    
    if time_of_day == 'Morning' or 'Afternoon':
        day = True
    else:
        day = False

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
    return render(request, 'home.html', {
        "length_cw" : length_cw,
        "current_year": current_year,
        "form": form,
        "submitted": submitted,
        "now" : now,
        "day_of_the_week": weekdays[current_weekday],
        "current_weather": current_weather,
        "unit_value": units_value,
        "weather_main_report" : wd,
        'to_celsius': cw_int,
        "city_name" : city_name,
        "weather_description" : weather_description,
        "min_temp" : min_temp,
        "visual" : visual,
        "max_temp" : max_temp,
        "humidity" : humidity,
        "wind_speed" : wind_speed,
        "wind_dir" : wind_dir,
        "side_forecast_month" : f_h_month,
        "side_forecast_day" : f_h_day,
        "first_hour_time" : f_h_time,
        "first_hour_max" : f_h_max,
        "first_hour_min" : f_h_min,
        "time_of_day" : day,
        "time_of_day2" : time_of_day,
        "first_hour_d" : first_hour_d,
        "second_hour_d" : second_hour_d,
        "third_hour_d" : third_hour_d,
    })



def searched(request):    
    if request.method == "POST":
        searched = request.POST["searched-location"]
        return render(request, 'searched.html', {'searched_location': searched})
    else:
        return render(request, 'searched.html', {})
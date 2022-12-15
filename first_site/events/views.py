from django.shortcuts import render, redirect
from datetime import *
from .forms import SubListForm
from django.http import HttpResponseRedirect
import random
from django.contrib import messages
import json
import datetime
from os import environ
import requests


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



# function to call to get data on the current forecast
def get_current_day_weather(city="Arlington", units="imperial"):
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = environ.get("CEJ_Weather_API")
    CITY = city
    UNITS = units
    
    first_api_call = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units={UNITS}"
    
    response1 = requests.get(first_api_call).json()
    response1_prettyprint = json.dumps(response1, indent=3)
    
    try:
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
            
    except KeyError:
        'none'
    
        
        
    try:
        return get_weather_report, current_temp, min_temp, max_temp, humidity, wind_speed, CompassDir, LON, LAT, visual
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



# function to call to get data on the weekly forecast
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
    



def home(request, location="arlington"):
    # Section for LIVE CAMERAS 
    LF1, LF2, LF3, LF4, LF5 = shuffle_live_cameras()
    
    
    # weather calls 
    # current_weather = str(get_current_day_weather()[1]).split(".")[0]
    current_weather = "65"
    length_cw = len(current_weather)
    cw_int = (int(current_weather) - 32) * 5/9
    cw_int = str(cw_int).split('.')[0]
    
    # city_name = str(get_current_day_weather()[10])
    city_name = "Bonadelle Ranchos-Madera Ranchos"
    wd = "Clear Sky"
    # weather_description = str(get_current_day_weather()[11])
    weather_description = "clear sky"
    # min_temp = str(get_current_day_weather()[2]).split(".")[0]
    min_temp = "105"
    str_minTemp = (int(min_temp) - 32) * 5/9
    met_min_temp = str(str_minTemp).split('.')[0]
    # max_temp = str(get_current_day_weather()[3]).split(".")[0]
    max_temp = "58"
    str_maxTemp = (int(max_temp) - 32) * 5/9
    met_max_temp = str(str_maxTemp).split('.')[0]
    # humidity = str(get_current_day_weather()[4]) + "%"
    humidity = "58%"
    # wind_speed = str(get_current_day_weather()[5])
    wind_speed = "105"
    str_windSpeed = (int(wind_speed) * 1.609)
    met_windSpeed = str(str_windSpeed).split('.')[0]
    # wind_dir = str(get_current_day_weather()[6])
    wind_dir = "NNW"
    # visual = str(get_current_day_weather()[12])
    visual = "10000"
    convert_wind = int(visual) // 1609
    visual = str(convert_wind)
    
    str_visual = (int(visual) * 1.609)
    met_visual = str(str_visual).split('.')[0]
    
    
    
    # cc_lon = get_current_day_weather()[7]
    cc_lon = "-97.10"
    # cc_lat = get_current_day_weather()[8]
    cc_lat = "32.73"
    # API call for the main weather widget
    # w_main, current_weather, min_temp, max_temp, humidity, wind_speed, wind_dir, cc_lon, cc_lat, current_date, city_name, wd, visual  = get_current_day_weather()[0]
    
    first_hour_d = 'light intensity shower rain'
    
    # API call for the ~FIRST HOUR~ side weather widget
    # f_h_month, f_h_day, f_h_time, f_h_max, f_h_min, f_h_des = weather_next_few_hours(cc_lat, cc_lon)[0]
    f_h_month, f_h_day, f_h_time, f_h_des, f_h_max, f_h_min = ("11", "30", "3:01:pm", "light rain", "101", "91")
    # Metric convert for side first hour
    toIntFirst = int(f_h_max) 
    convert_f_h = (toIntFirst - 32) * 5/9
    metric_first_hour_max = str(convert_f_h).split('.')[0]
    toIntFirst2 = int(f_h_max) 
    convert_f_h2 = (toIntFirst2 - 32) * 5/9
    metric_first_hour_min = str(convert_f_h2).split('.')[0]
    
    
    # API call for the ~SECOND HOUR~ side weather widget
    # s_h_month, s_h_day, s_h_time, s_h_max, s_h_min, s_h_des = weather_next_few_hours(cc_lat, cc_lon)[1]
    s_h_month, s_h_day, s_h_time, s_h_des, s_h_max, s_h_min = ("11", "30", "6:00:pm", "clear sky", "102", "92")
    # Metric convert for side first hour 
    toIntSecond = int(s_h_max) 
    convert_s_h = (toIntSecond - 32) * 5/9
    metric_second_hour_max = str(convert_s_h).split('.')[0]
    toIntSecond2 = int(s_h_min) 
    convert_s_h2 = (toIntSecond2 - 32) * 5/9
    metric_second_hour_min = str(convert_s_h2).split('.')[0]
    
    
    # API call for the ~THIRD HOUR~ side weather widget
    # t_h_month, t_h_day, t_h_time, t_h_max, t_h_min, t_h_des = weather_next_few_hours(cc_lat, cc_lon)[2]
    t_h_month, t_h_day, t_h_time, t_h_des, t_h_max, t_h_min = ('11', '30', '9:00:pm', 'rain', '103', '93')
    toIntThird = int(t_h_max)
    convert_t_h = (toIntThird - 32) * 5/9
    metric_third_hour_max = str(convert_t_h).split('.')[0]
    toIntThird2 = int(t_h_min)
    convert_t_h2 = (toIntThird2 - 32) * 5/9
    metric_third_hour_min = str(convert_t_h2).split('.')[0]


    # API call for the FIRST weekly forecast DAY
    # weekly_d1_des, weekly_d1_max, weekly_d1_min, weekly_d1_date, weekly_d1_day  = coming_days(cc_lat, cc_lon)['day1']
    weekly_d1_des, weekly_d1_max, weekly_d1_min, weekly_d1_date, weekly_d1_day  = ('clear sky', '101', '91', 'date', 'idk')
    # for converting day one max imperial to metric 
    weekly_d1_max_metric = (int(weekly_d1_max) - 32) * 5/9
    weekly_d1_max_metric_str = str(weekly_d1_max_metric).split('.')[0]
    # for converting day one max metric to imperial
    weekly_d1_min_metric = (int(weekly_d1_min) - 32) * 5/9
    weekly_d1_min_metric_str = str(weekly_d1_min_metric).split('.')[0]
    
    
    # API call for the SECOND weekly forecast DAY
    # weekly_d2_des, weekly_d2_max, weekly_d2_min, weekly_d2_date, weekly_d2_day  = coming_days(cc_lat, cc_lon)['day2']
    weekly_d2_des, weekly_d2_max, weekly_d2_min, weekly_d2_date, weekly_d2_day  = ('light rain', '102', '92', 'date', 'idk')
    # for converting day one max imperial to metric 
    weekly_d2_max_metric = (int(weekly_d2_max) - 32) * 5/9
    weekly_d2_max_metric_str = str(weekly_d2_max_metric).split('.')[0]
    # for converting day one max metric to imperial
    weekly_d2_min_metric = (int(weekly_d2_min) - 32) * 5/9
    weekly_d2_min_metric_str = str(weekly_d2_min_metric).split('.')[0]
    
    
    # API call for the THIRD weekly forecast DAY
    # weekly_d3_des, weekly_d3_max, weekly_d3_min, weekly_d3_date, weekly_d3_day  = coming_days(cc_lat, cc_lon)['day3']
    weekly_d3_des, weekly_d3_max, weekly_d3_min, weekly_d3_date, weekly_d3_day  = ('thunderstorm', '103', '93', 'date', 'idk')
    # for converting day one max imperial to metric 
    weekly_d3_max_metric = (int(weekly_d3_max) - 32) * 5/9
    weekly_d3_max_metric_str = str(weekly_d3_max_metric).split('.')[0]
    # for converting day one max metric to imperial
    weekly_d3_min_metric = (int(weekly_d3_min) - 32) * 5/9
    weekly_d3_min_metric_str = str(weekly_d3_min_metric).split('.')[0]
    
    
    # API call for the FOURTH weekly forecast DAY
    # weekly_d4_des, weekly_d4_max, weekly_d4_min, weekly_d4_date, weekly_d4_day  = coming_days(cc_lat, cc_lon)['day4']
    weekly_d4_des, weekly_d4_max, weekly_d4_min, weekly_d4_date, weekly_d4_day  = ('light rain', '104', '94', 'date', 'idk')
    # for converting day one max imperial to metric 
    weekly_d4_max_metric = (int(weekly_d4_max) - 32) * 5/9
    weekly_d4_max_metric_str = str(weekly_d4_max_metric).split('.')[0]
    # for converting day one max metric to imperial
    weekly_d4_min_metric = (int(weekly_d4_min) - 32) * 5/9
    weekly_d4_min_metric_str = str(weekly_d4_min_metric).split('.')[0]
    
    
    
    
    
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
            
            
    now = datetime.datetime.now()
    current_year = now.year
    current_day = now.day
    current_month = now.month
    current_weekday = now.weekday()
    
    
    day_time = get_time_of_day()[0] # False/True
    time_of_day = get_time_of_day()[2] # Day of the week
    
    days_ahead = get_next_day(time_of_day)
    d1, d2, d3, d4, d5, d6 = days_ahead
    
    
    timesOfDay = get_time_of_day()[1]

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
        
        # first side hour variables
        "side_forecast_month" : f_h_month,
        "side_forecast_day" : f_h_day,
        "first_hour_time" : f_h_time,
        "first_hour_description" : f_h_des,
        "first_hour_max" : f_h_max,
        "first_hour_min" : f_h_min,
        "metric_first_hour_max" : metric_first_hour_max,
        "metric_first_hour_min" : metric_first_hour_min,

        # second side hour variables
        "second_hour_max" : s_h_max,
        "second_hour_min" : s_h_min,
        "second_hour_month" : s_h_month,
        "second_hour_day": s_h_day,
        "second_hour_description" : s_h_des,
        "second_hour_time" : s_h_time,
        "metric_second_hour_max" : metric_second_hour_max,
        "metric_second_hour_min" : metric_second_hour_min,
        
        # third side hour variables
        "third_hour_max" : t_h_max,
        "third_hour_min" : t_h_min,
        "third_hour_month" : s_h_month,
        "third_hour_day" : t_h_day,
        "third_hour_time" : t_h_time,
        "third_hour_description" : t_h_des,
        "metric_third_hour_max" : metric_third_hour_max,
        "metric_third_hour_min" : metric_third_hour_min,
        
        
        # weekly forecast day 1 variables
        "weekly_description_d1" : weekly_d1_des,
        "weekly_d1_max_temp" : weekly_d1_max,
        "weekly_d1_min_temp" : weekly_d1_min,
        "weekly_d1_metric_max" : weekly_d1_max_metric_str,
        "weekly_d1_metric_min" : weekly_d1_min_metric_str,
        
        
        # weekly forecast day 2 variables
        "weekly_description_d2" : weekly_d2_des,
        "weekly_d2_max_temp" : weekly_d2_max,
        "weekly_d2_min_temp" : weekly_d2_min,
        "weekly_d2_metric_max" : weekly_d2_max_metric_str,
        "weekly_d2_metric_min" : weekly_d2_min_metric_str,
        
        
        # weekly forecast day 3 variables
        "weekly_description_d3" : weekly_d3_des,
        "weekly_d3_max_temp" : weekly_d3_max,
        "weekly_d3_min_temp" : weekly_d3_min,
        "weekly_d3_metric_max" : weekly_d3_max_metric_str,
        "weekly_d3_metric_min" : weekly_d3_min_metric_str,
        
        
        # weekly forecast day 4 variables
        "weekly_description_d4" : weekly_d4_des,
        "weekly_d4_max_temp" : weekly_d4_max,
        "weekly_d4_min_temp" : weekly_d4_min,
        "weekly_d4_metric_max" : weekly_d4_max_metric_str,
        "weekly_d4_metric_min" : weekly_d4_min_metric_str,
        
        
        
        "time_of_day" : day1,
        "time_of_day2" : timesOfDay, # variable for good 'moring' on home page
        "first_hour_d" : first_hour_d,
        "second_hour_d" : second_hour_d,
        "third_hour_d" : third_hour_d,
        "met_min_temp" : met_min_temp,
        "met_max_temp" : met_max_temp,
        "met_windSpeed" : met_windSpeed,
        "met_visual" : met_visual,
        "next_day_one" : d1,
        "next_day_two" : d2,
        "next_day_three" : d3,
        "next_day_four" : d4,
        
        
        # live camera variables
        "lf1" : LF1,
        "lf2" : LF2,
        "lf3" : LF3,
    })








def searched(request):
    if request.method == "POST":
        searched = request.POST["searched-location"]
        
        #****************************#
        # testing to see if the user has made the change to either metric or imperial
        units_value = '0'
        imperial_value = request.POST.get('imperial')
        metric_value = request.POST.get('metric')
    
        if metric_value == '0':
            units_value = '1'
        elif metric_value == '1':
            units_value = '0'
        #****************************#
        
        
        
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
            
        
    
        return render(request, 'searched.html', {
            "units_value" : units_value,
            "searched_location" : searched,
            })
        
    
    else:
        return render(request, 'searched.html', {})
    
    



def about(request):
    return render(request, 'about.html', {})
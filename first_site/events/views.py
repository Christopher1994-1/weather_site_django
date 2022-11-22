from django.shortcuts import render
from datetime import *
from .forms import SubListForm
from django.http import HttpResponseRedirect
from django.contrib import messages
import calendar


def home(request, location="arlington"):
    
    name = "John"
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
        "first_name": name,
        "current_year": current_year,
        "form": form,
        "submitted": submitted,
        "now" : now,
        "day_of_the_week": weekdays[current_weekday],
    })



def searched(request):    
    if request.method == "POST":
        searched = request.POST["searched-location"]
        return render(request, 'searched.html', {'searched_location': searched})
    else:
        return render(request, 'searched.html', {})
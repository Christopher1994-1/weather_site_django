from django.shortcuts import render
from datetime import *


def home(request, location="arlington"):
    name = "John"
    now = datetime.now()
    current_year = now.year
    
    return render(request, 'home.html', {
        "first_name": name,
        "current_year": current_year,
    })

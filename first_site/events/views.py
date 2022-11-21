from django.shortcuts import render
from datetime import *
from .forms import SubListForm
from django.http import HttpResponseRedirect




def home(request, location="arlington"):
    
    name = "John"
    submitted = False
    if request.method == "POST":
        form = SubListForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/home?submitted=True')
    else:
        form = SubListForm()
        if 'submitted' in request.GET:
            submitted = True
            
            
    now = datetime.now()
    current_year = now.year
    form = SubListForm    
    return render(request, 'home.html', {
        "first_name": name,
        "current_year": current_year,
        "form": form,
        "submitted": submitted
    })

from django import forms
from django.forms import ModelForm
from .models import SubList



# Create form

class SubListForm(ModelForm):
    class Meta:
        model = SubList
        fields = "__all__"
     
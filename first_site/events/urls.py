from django.urls import path
from . import views

# Path Converters
# int: Integers
# str: Strings
# path: whole urls /
# slug: hyphen-and_underscores_stuff
# UUID: universally unique identifier

urlpatterns = [
    path('', views.home, name="home"),
    path('<str:location>', views.home, name="home"),
    path('<slug:location>', views.home, name="home"),
    path('searched/', views.searched, name="searched")
]

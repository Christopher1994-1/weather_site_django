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
    path('searched/', views.searched, name="searched"),
    path('metric_button', views.metric_button, name="metric_button"),
    path('imperial_button', views.imperial_button, name="imperial_button"),
    path('about/', views.about, name="about"),
    path('news/', views.news, name="news"),
    path('live_cameras/', views.live_cameras, name="live_cameras"),
]




from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def Homeview(request):

    url = "http://api.openweathermap.org/data/2.5/weather?q={}&APPID=ae051d120236e4e4bb59ebda98f367df"

    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_list = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            }
        weather_list.append(city_weather)
    
    context = {'weather_list': weather_list, 'form': form}
    return render(request, 'home.html', context)
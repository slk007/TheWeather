from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def Homeview(request):

    url = "http://api.openweathermap.org/data/2.5/weather?q={}&APPID=ae051d120236e4e4bb59ebda98f367df"

    error_message = ''
    message = ''
    message_class = ''

    if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():

            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                api_response = requests.get(url.format(new_city)).json()
        
                if api_response['cod'] == 200:
                    form.save()
                else:
                    error_message = 'Invalid city name!!! Try again!!'
            else:
                error_message = 'City already exists on the Page'
            
        if error_message:
            message = error_message
            message_class = 'is-danger'
        else:
            message = "City added succesfully !!"
            message_class = 'is-success'

    
    form = CityForm()

    cities = City.objects.all().order_by('-id')

    weather_list = []

    for city in cities:
        api_response = requests.get(url.format(city)).json()
        city_weather = {
            'city': city,
            'temperature': int(api_response['main']['temp']-273.15),
            'description': api_response['weather'][0]['description'],
            'icon': api_response['weather'][0]['icon'],
            }
        weather_list.append(city_weather)
    
    context = {
        'weather_list': weather_list,
        'form': form,
        'message': message,
        'message_class': message_class
        }
    return render(request, 'home.html', context)



def DeleteCityView(request, city_name):

    city = City.objects.filter(name=city_name)
    city.delete()

    return redirect('home')
import os
from django.shortcuts import render, redirect
import requests
import json
from .models import City
from .forms import CityForm
# Create your views here.
def index(request):
    secrets_path = os.path.join(os.path.dirname(__file__), 'secrets.json')
    with open(secrets_path) as secrets_file:
        secrets = json.load(secrets_file)
        API_KEY = secrets.get('API_KEY', None)
    if not API_KEY:
        raise ValueError("API_KEY not found in secrets.json")
    
    url = f'http://api.openweathermap.org/data/2.5/weather?q={{}}&units=metric&appid={API_KEY}'
    
    cities = City.objects.all()
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name']
            existing_city = City.objects.filter(name=city_name).first()
            if not existing_city:
                # Add the city to the database
                new_city = City(name=city_name)
                new_city.save()
    
    form = CityForm()
    weather_data = []
    
    for city in cities:
        
    
        city_weather = requests.get(url.format(city)).json()
        weather = {
        'city' : city,
        'temperature' : city_weather['main']['temp'],
        'feel' : city_weather['main']['feels_like'],
        'humidity' : city_weather['main']['humidity'],
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)
    context = {'weather_data':weather_data,'form':form}
    
    return render(request, 'weather/index.html',context)
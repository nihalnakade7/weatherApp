from django.shortcuts import render
import requests

# Create your views here.

def index(request):

    if request.method == 'POST':
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=5d07e8d1849479eda02c5b87bc1d53d7'
        city = request.POST['city']
        print(city)

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        contex = {"city_weather" : city_weather}


        return render(request,'index.html',contex)

    return render(request,'index.html')
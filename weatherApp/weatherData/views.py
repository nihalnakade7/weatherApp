from django.shortcuts import render
import requests
from .models import City
from django.contrib import messages


# Create your views here.

def getData(username):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=5d07e8d1849479eda02c5b87bc1d53d7'
    weather_data = []
    cities = City.objects.all().filter(username = username)

    for city in cities:

    #city = "nagpur"
        r = requests.get(url.format(city)).json()

        #print(r)

        city_weather = {
            'city' : city,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)
    return weather_data

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=5d07e8d1849479eda02c5b87bc1d53d7'
    username = request.session.get('username',None)
    print(username)
    if request.method == 'POST':
        if username is not None:
        
            city = request.POST['city']
            print(city)
            
            r = requests.get(url.format(city)).json()
            if r['cod'] == 404:
                contex = {"error" : "City Not Found"}
                return render(request,'index.html',contex)

            if r['cod'] == 200:
                print(200)
                f = City.objects.filter(city = city)
                if f:
                    weather_data = getData(username) 
                    contex = {"weather_data" : weather_data}

                    return render(request,'index.html',contex)


                obj = City(city = city,username = username)
                obj.save()

                weather_data = getData(username)    

                contex = {"weather_data" : weather_data}

                return render(request,'index.html',contex)
        else:
            messages.info(request,"Please Login First")
            return render(request,'accounts/login.html')

    if request.method == 'GET':

        if 'username' in request.session:
            username = request.session.get('username',None)
            weather_data = getData(username)    

            contex = {"weather_data" : weather_data}

            return render(request,'index.html',contex)

        else:


            weather_data = []
            '''cities = City.objects.all()

            for city in cities:

            #city = "nagpur"
                r = requests.get(url.format(city)).json()

                #print(r)

                city_weather = {
                    'city' : city,
                    'temperature' : r['main']['temp'],
                    'description' : r['weather'][0]['description'],
                    'icon' : r['weather'][0]['icon'],
                }

                weather_data.append(city_weather)'''

            contex = {"weather_data" : weather_data}

        return render(request,'index.html',contex)
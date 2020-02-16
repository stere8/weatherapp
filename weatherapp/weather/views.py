import requests
from django.shortcuts import render
from .models import city as citi
from django.http import HttpResponseRedirect, Http404


# Create your views here.


def home(request, units='metric', message=None):
    context = []
    cities = citi.objects.all()
    weather_data = []
    if units == 'imperial':
        measure = '°F'
    elif units == 'metric':
        measure = '°C'
    else:
        raise Http404
    for city in cities:
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city.name + '&units=' + units + '&appid=a7fe874c8ca9992dc4bf58cbce8bdc72'
        r = requests.get(url).json()
        city_weather = {
            'id': city.id,
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            'measure': measure
        }
        weather_data.append(city_weather)
        context = {'weather_data': weather_data}
        if message:
            context['message'] = message
    return render(request, 'home.html', context)


def delete(request, pk):
    focused = citi.objects.get(id=pk)
    focused.delete()
    return HttpResponseRedirect('/')


def add(request):
    name = request.POST.get('city')
    if name:
        old_cities = citi.objects.all()
        for old_city in old_cities:
            if name == old_city.name:
                message = 'The City %s already exists' % name
                return home(request, message=message)
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' + name + '&units=imperial&appid=a7fe874c8ca9992dc4bf58cbce8bdc72'
        r = requests.get(url).json()
        if r['cod'] == '404':
            message = 'The city %s doesn\'t exist' % name
            return home(request, message=message)
        new_citi = citi(name=name)
        new_citi.save()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def error_404(request,exceptions):
    exceptions = "Error page Not found"
    context = {'exception':exceptions }
    return render(request, '404.html', context)

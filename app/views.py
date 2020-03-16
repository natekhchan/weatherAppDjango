from django.shortcuts import render
from darksky import forecast
from datetime import date, timedelta, datetime

from ipstack import GeoLookup
import requests
import json

# Create your views here.

def home(request):

    # city = 42.3601, 71.0589
    geo_lookup = GeoLookup("40d5d9284ed678d9bba68017704770bc")
    location = geo_lookup.get_own_location()

    lat = location['latitude']
    lng = location['longitude']
    region = location['region_name']

    city = lat,lng

    print(location)

    weekday = date.today()

    weekly_weather = {}
    hourly_weather = {}


    with forecast('fcbb70ecadd8b48599aca7e92529bf30',*city, units="si") as city:
        for day in city.daily:
            day = dict(day = date.strftime(weekday, '%A'), sum=day.summary,tempMin=round(day.temperatureMin),tempMax=round(day.temperatureMax))
            print('{day} ---- {sum} -- {tempMin} - {tempMax}'.format(**day))
            weekday += timedelta(days=1)

            pic = ''
            summary = ('{sum}'.format(**day).lower())

            if 'drizzle' in summary:
                pic = 'rain.png'
            elif 'rain' in summary:
                pic = 'rain.png'
            elif 'cloudy' in summary:
                pic = 'clouds.png'
            elif 'clear' in summary:
                pic = 'sun.png'
            elif 'partly cloudy' in summary:
                pic = 'partly-cloudy-day.png'
            elif 'humid' in summary:
                pic = 'partly-cloudy-day.png'
            else:
                pic = 'clouds.png'

            weekly_weather.update({'{day}'.format(**day):{'tempMin':'{tempMin}'.format(**day),'tempMax':'{tempMax}'.format(**day),'pic':pic}})

    today = weekly_weather[(date.today().strftime("%A"))]
    del weekly_weather[(date.today().strftime("%A"))]

    print(today.get("tempMax"))

    hour = datetime.now().hour
    location = forecast('fcbb70ecadd8b48599aca7e92529bf30',lat, lng, units="si")
    i = 0

    hour_ = ''

    while hour < 24:
        temp = round(location.hourly[i].temperature)

        pic = ''
        summary = location.hourly[i].summary.lower()

        if 'drizzle' in summary:
            pic = 'rain.png'
        elif 'rain' in summary:
            pic = 'rain.png'
        elif 'cloudy' in summary:
            pic = 'clouds.png'
        elif 'clear' in summary:
            pic = 'sun.png'
        elif 'partly cloudy' in summary:
            pic = 'partly-cloudy-day.png'
        elif 'humid' in summary:
            pic = 'partly-cloudy-day.png'
        else:
            pic = 'clouds.png'

        if hour < 12:
            hour_ = '{}am'.format(hour)
            hourly_weather.update({hour_:{'pic':pic,'temp':temp}})
        else:
            hour_ = '{}pm'.format(hour-12)
            hourly_weather.update({hour_:{'pic':pic,'temp':temp}})



        hour+=1
        i+=1

    return render(request,'home.html',{'weekly_weather':weekly_weather,'hourly_weather':hourly_weather,'today':today,'region':region})
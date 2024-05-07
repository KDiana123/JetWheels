import math
from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from car.models import Car
from flight.models import Place


# Create your views here.
def car_index(request):
    return render(request, 'car/index.html')


@csrf_exempt
def car(request):
    o_place = request.GET.get('Origin')
    departdate = request.GET.get('DepartDate')
    depart_date = datetime.strptime(departdate, "%Y-%m-%d")
    returndate = request.GET.get('ReturnDate')
    return_date = datetime.strptime(returndate, "%Y-%m-%d")
    difference = return_date - depart_date

    days = difference.days
    pickup_place = Place.objects.get(code=o_place.upper())  ##
    cars = Car.objects.filter(pickup_location_id=pickup_place.id)
    return render(request, "car/search.html", {
        'cars': cars,
        'pickup_place': pickup_place,
        'destination': "",
        'seat': "",
        'trip_type': 1,
        'depart_date': depart_date,
        'return_date': return_date,
        'max_price': math.ceil(1 / 100) * 100,
        'min_price': math.floor(1 / 100) * 100,
        'days': days
    })


def review(request):
    flight_1 = request.GET.get('flight1Id')
    date1 = request.GET.get('flight1Date')
    date2 = request.GET.get('flight2Date')
    pickup_place = request.GET.get('pickupLocation')
    days = request.GET.get('days')
    if request.user.is_authenticated:
        flight1 = Car.objects.get(id=flight_1)
        flight1ddate = date1
        flight1adate = date1

        flight2ddate = date2
        flight2adate = date2

        return render(request, "car/book.html", {
            'flight1': flight1,
            'flight2': None,
            "flight1ddate": flight1ddate,
            "flight1adate": flight1adate,
            "flight2ddate": flight2ddate,
            "flight2adate": flight2adate,
            "seat": 1,
            "fee": 100,
            "pickup_place": pickup_place,
            "duration": days
        })

    else:
        return HttpResponseRedirect(reverse("login"))
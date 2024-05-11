import math
import secrets
from datetime import datetime
from io import BytesIO

from django.db.models import Count, Sum
from django.db.models.functions import TruncDay
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from chartjs.views.lines import BaseLineChartView
from xhtml2pdf import pisa

from car.models import Car, Order
from flight.models import Place, Flight, Ticket


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
    cars = Car.objects.filter(pickup_location_id=pickup_place.id).order_by('price')

    min_price = cars.first().price if cars else None
    max_price = cars.last().price if cars else None
    return render(request, "car/search.html", {
        'cars': cars,
        'pickup_place': pickup_place,
        'destination': "",
        'seat': "",
        'trip_type': 1,
        'depart_date': depart_date,
        'return_date': return_date,
        'max_price': math.ceil((max_price * days) / 100) * 100,
        'min_price': math.floor((min_price* days) / 100) * 100,
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


def book(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            flight_1 = request.POST.get('flight1')
            flight_1date = request.POST.get('flight1Date')
            flight_2date = request.POST.get('flight2Date')
            duration = request.POST.get('duration')

            countrycode = request.POST['countryCode']
            mobile = request.POST['mobile']
            email = request.POST['email']
            c_car = Car.objects.get(id=flight_1)

            try:
                order = Order.objects.create(
                    user_id=request.user.id,
                    email=email,
                    phone="+" + countrycode + mobile,
                    car_id=c_car.id,
                    pickup_date=datetime.strptime(flight_1date, '%d-%m-%Y'),
                    dropoff_date=datetime.strptime(flight_2date, '%d-%m-%Y'),
                    total_amount=c_car.price * int(duration),
                    ref_no=secrets.token_hex(4).upper()
                )
            except Exception as e:
                return HttpResponse(e)

            return render(request, "car/payment.html", {
                'ticket': order.order_id,
                'fare': c_car.price * int(duration)
            })
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponse("Method must be post.")


def payment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            ticket_id = request.POST['ticket']
            t2 = False
            if request.POST.get('ticket2'):
                ticket2_id = request.POST['ticket2']
                t2 = True
            fare = request.POST.get('fare')
            card_number = request.POST['cardNumber']
            card_holder_name = request.POST['cardHolderName']
            exp_month = request.POST['expMonth']
            exp_year = request.POST['expYear']
            cvv = request.POST['cvv']

            try:
                ticket = Order.objects.get(order_id=ticket_id)
                ticket.status = 'PAID'
                ticket.save()

                return render(request, 'car/payment_process.html', {
                    'ticket1': ticket,
                })
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be post.")
    else:
        return HttpResponseRedirect(reverse('login'))


def ticket_data(request, ref):
    ticket = Order.objects.get(order_id=ref)

    return JsonResponse({
        'ref': ticket.order_id,
        'status': ticket.status
    })

@csrf_exempt
def cancel_ticket(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ref = request.POST['ref']
            try:
                ticket = Order.objects.get(ref_no=ref)
                if ticket.user == request.user:
                    ticket.status = 'CANCELLED'
                    ticket.save()
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({
                        'success': False,
                        'error': "User unauthorised"
                    })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': e
                })
        else:
            return HttpResponse("User unauthorised")
    else:
        return HttpResponse("Method must be POST.")


def dashboard(request):
    # Статистика по заказам
    popular_cars = Order.objects.values('car__car_name').annotate(total_orders=Count('car')).order_by('-total_orders')[:5]

    # Статистика по полетам
    popular_routes = Flight.objects.values('origin_id__city', 'destination_id__city').annotate(total_flights=Count('id')).order_by('-total_flights')[:5]

    # Статистика по самолетам
    popular_planes = Flight.objects.values('plane').annotate(total_flights=Count('id')).order_by('-total_flights')[:5]

    # Количество заказов по дням
    orders_by_day = Order.objects.annotate(day=TruncDay('pickup_date')).values('day').annotate(total=Count('car_id')).order_by('day')

    # Общая сумма заказов по дням
    total_amount_by_day = Order.objects.annotate(day=TruncDay('pickup_date')).values('day').annotate(total=Sum('total_amount')).order_by('day')

    # Распределение цен на автомобили
    price_distribution = Car.objects.values('car_name').annotate(total_price=Sum('price'))

    # Статистика по продажам билетов
    ticket_sales_by_date = Ticket.objects.annotate(date=TruncDay('booking_date')).values('date').annotate(total_tickets=Count('id')).order_by('date')

    context = {
        'popular_cars': popular_cars,
        'popular_routes': popular_routes,
        'popular_planes': popular_planes,
        'orders_by_day': orders_by_day,
        'total_amount_by_day': total_amount_by_day,
        'price_distribution': price_distribution,
        'ticket_sales_by_date': ticket_sales_by_date,
    }
    return render(request, 'analytics.html', context)


class OrdersByDayChart(BaseLineChartView):
    def get_labels(self):
        return [d['day'].strftime('%Y-%m-%d') for d in self.data]

    def get_providers(self):
        return ["Orders"]

    def get_data(self):
        return [[d['total'] for d in self.data]]


class TotalAmountByDayChart(BaseLineChartView):
    def get_labels(self):
        return [d['day'].strftime('%Y-%m-%d') for d in self.data]

    def get_providers(self):
        return ["Total Amount"]

    def get_data(self):
        return [[d['total'] for d in self.data]]


class PriceDistributionChart(BaseLineChartView):
    def get_labels(self):
        return [p['car_name'] for p in self.data]

    def get_data(self):
        return [p['total_price'] for p in self.data]


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result, encoding='utf-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@csrf_exempt
def get_ticket(request):
    ref = request.GET.get("ref")
    order = Order.objects.get(ref_no=ref)
    data = {
        'order': order,
        'current_year': datetime.now().year
    }
    pdf = render_to_pdf('car/ticket.html', data)
    return HttpResponse(pdf, content_type='application/pdf')
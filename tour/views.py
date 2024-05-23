import math
import secrets
from audioop import reverse
from datetime import datetime
from io import BytesIO

from django.db.models import Count, F
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa

from flight.models import Place
from tour.models import Tour, Reservation


# Create your views here.


def tour_index(request):
    return render(request, 'tour/index.html')


@csrf_exempt
def tour(request):
    o_place = request.GET.get('Origin')
    departdate = request.GET.get('DepartDate')
    depart_date = datetime.strptime(departdate, "%Y-%m-%d")

    pickup_place = Place.objects.get(code=o_place.upper())  ##
    tour = Tour.objects.annotate(
        reserved_capacity=Count('reservation')
    ).filter(
        location_id=pickup_place.id,
        start_date__gte=depart_date,
        reserved_capacity__lt=F('tour_capacity')  # Убираем туры, где забронированное количество равно капасити
    ).order_by('price')

    min_price = tour.first().price if tour else None
    max_price = tour.last().price if tour else None
    return render(request, "tour/search.html", {
        'tours': tour,
        'pickup_place': pickup_place,
        'destination': "",
        'seat': "",
        'trip_type': 1,
        'depart_date': depart_date,
        'max_price': math.ceil(max_price / 100) * 100 if max_price else None,
        'min_price': math.floor(min_price / 100) * 100 if min_price else None,
    })


def review(request):
    flight_1 = request.GET.get('flight1Id')
    date1 = request.GET.get('flight1Date')
    date2 = request.GET.get('flight2Date')
    pickup_place = request.GET.get('pickupLocation')
    days = request.GET.get('days')
    if request.user.is_authenticated:
        flight1 = Tour.objects.get(id=flight_1)
        flight1ddate = date1
        flight1adate = date1

        flight2ddate = date2
        flight2adate = date2

        return render(request, "tour/book.html", {
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

            countrycode = request.POST['countryCode']
            mobile = request.POST['mobile']
            email = request.POST['email']
            c_tour = Tour.objects.get(id=flight_1)

            try:
                order = Reservation.objects.create(
                    guest_id=request.user.id,
                    email=email,
                    phone="+" + countrycode + mobile,
                    tour_id=c_tour.id,
                    total_amount=c_tour.price,
                    ref_no=secrets.token_hex(4).upper()
                )
            except Exception as e:
                return HttpResponse(e)

            return render(request, "car/payment.html", {
                'ticket': order.id,
                'fare': c_tour.price
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
                ticket = Reservation.objects.get(id=ticket_id)
                ticket.status = 'PAID'
                ticket.save()

                return render(request, 'tour/payment_process.html', {
                    'ticket1': ticket,
                })
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be post.")
    else:
        return HttpResponseRedirect(reverse('login'))


def ticket_data(request, ref):
    ticket = Reservation.objects.get(id=ref)

    return JsonResponse({
        'ref': ticket.id,
        'status': ticket.status
    })

@csrf_exempt
def get_ticket(request):
    ref = request.GET.get("ref")
    order = Reservation.objects.get(ref_no=ref)
    data = {
        'order': order,
        'current_year': datetime.now().year
    }
    pdf = render_to_pdf('tour/ticket.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result, encoding='utf-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def details(request, tour_id):
    tour_detail = get_object_or_404(Tour, id=tour_id)
    return render(request, 'tour/details.html', {
        'tour': tour_detail,
    })

# tour/views.py
from django.shortcuts import render
from .forms import ServiceMetricsForm
import math

def calculate_service_rate(avg_service_time):
    return 1 / avg_service_time

def calculate_traffic_intensity(avg_arrival_rate, num_channels):
    return avg_arrival_rate / num_channels

def calculate_idle_probability(traffic_intensity):
    return 1 - traffic_intensity

def calculate_rejection_probability(traffic_intensity, num_channels):
    return (traffic_intensity ** (num_channels + 1)) / math.factorial(num_channels)

def calculate_service_probability(traffic_intensity, num_channels):
    return 1 - calculate_rejection_probability(traffic_intensity, num_channels)

def calculate_avg_busy_channels(traffic_intensity, num_channels):
    return traffic_intensity * calculate_service_probability(traffic_intensity, num_channels)

def calculate_avg_queue_length(traffic_intensity, num_channels):
    p0 = calculate_idle_probability(traffic_intensity)
    return (traffic_intensity * num_channels * p0) / (math.factorial(num_channels) * (1 - traffic_intensity / num_channels) * 2)

def calculate_avg_system_length(traffic_intensity, num_channels):
    return calculate_avg_queue_length(traffic_intensity, num_channels) + calculate_avg_busy_channels(traffic_intensity, num_channels)

def calculate_absolute_throughput(avg_arrival_rate, avg_service_time, num_channels):
    traffic_intensity = calculate_traffic_intensity(avg_arrival_rate, num_channels)
    service_rate = calculate_service_rate(avg_service_time)
    return service_rate * (1 - calculate_rejection_probability(traffic_intensity, num_channels))

def calculate_relative_throughput(avg_arrival_rate, avg_service_time, num_channels):
    traffic_intensity = calculate_traffic_intensity(avg_arrival_rate, num_channels)
    service_rate = calculate_service_rate(avg_service_time)
    return (1 - calculate_rejection_probability(traffic_intensity, num_channels)) / num_channels

def calculate_avg_time_in_queue(avg_arrival_rate, avg_service_time, num_channels):
    traffic_intensity = calculate_traffic_intensity(avg_arrival_rate, num_channels)
    service_rate = calculate_service_rate(avg_service_time)
    return calculate_avg_queue_length(traffic_intensity, num_channels) / (avg_arrival_rate * (1 - calculate_rejection_probability(traffic_intensity, num_channels)))

def calculate_avg_time_in_system(avg_arrival_rate, avg_service_time, num_channels):
    traffic_intensity = calculate_traffic_intensity(avg_arrival_rate, num_channels)
    service_rate = calculate_service_rate(avg_service_time)
    return calculate_avg_system_length(traffic_intensity, num_channels) / (avg_arrival_rate * (1 - calculate_rejection_probability(traffic_intensity, num_channels)))

def calculate_avg_time_in_service(avg_service_time):
    return avg_service_time / 2

def service_metrics_view(request):
    if request.method == 'POST':
        form = ServiceMetricsForm(request.POST)
        if form.is_valid():
            avg_arrival_rate = form.cleaned_data['avg_arrival_rate']
            avg_service_time_minutes = form.cleaned_data['avg_service_time_minutes']
            num_channels = form.cleaned_data['num_channels']

            avg_service_time_hours = avg_service_time_minutes / 60
            service_rate = calculate_service_rate(avg_service_time_hours)
            traffic_intensity = calculate_traffic_intensity(avg_arrival_rate / 24, num_channels)

            idle_probability = calculate_idle_probability(traffic_intensity)
            rejection_probability = calculate_rejection_probability(traffic_intensity, num_channels)
            service_probability = calculate_service_probability(traffic_intensity, num_channels)
            avg_busy_channels = calculate_avg_busy_channels(traffic_intensity, num_channels)
            avg_queue_length = calculate_avg_queue_length(traffic_intensity, num_channels)
            avg_system_length = calculate_avg_system_length(traffic_intensity, num_channels)
            absolute_throughput = calculate_absolute_throughput(avg_arrival_rate / 24, avg_service_time_hours, num_channels)
            relative_throughput = calculate_relative_throughput(avg_arrival_rate / 24, avg_service_time_hours, num_channels)
            avg_time_in_queue = calculate_avg_time_in_queue(avg_arrival_rate / 24, avg_service_time_hours, num_channels)
            avg_time_in_system = calculate_avg_time_in_system(avg_arrival_rate / 24, avg_service_time_hours, num_channels)
            avg_time_in_service = calculate_avg_time_in_service(avg_service_time_minutes)

            context = {
                'form': form,
                'results': {
                    'idle_probability': idle_probability,
                    'rejection_probability': rejection_probability,
                    'service_probability': service_probability,
                    'avg_busy_channels': avg_busy_channels,
                    'avg_queue_length': avg_queue_length,
                    'avg_system_length': avg_system_length,
                    'absolute_throughput': absolute_throughput,
                    'relative_throughput': relative_throughput,
                    'avg_time_in_queue': avg_time_in_queue,
                    'avg_time_in_system': avg_time_in_system,
                    'avg_time_in_service': avg_time_in_service,
                }
            }
            return render(request, 'math_analytics.html', context)
    else:
        form = ServiceMetricsForm()

    return render(request, 'math_analytics.html', {'form': form})

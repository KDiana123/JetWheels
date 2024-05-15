from django.db import models

from flight import models as flight_models
# Create your models here.


class Tour(models.Model):
    tour_name = models.CharField(max_length=30, default="")
    tour_desc = models.CharField(max_length=300, default="")
    tour_included = models.CharField(max_length=300, default="")
    price = models.IntegerField(default=0)
    tour_capacity = models.IntegerField(default=10)
    location = models.ForeignKey(flight_models.Place, on_delete=models.CASCADE, related_name="location")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.tour_name


ORDER_STATUS = (
    ('PENDING', 'Pending'),
    ('PAID', 'Paid'),
    ('CONFIRMED', 'Confirmed'),
    ('CANCELLED', 'Cancelled'),
    ('CLOSED', 'Closed')
)


class Reservation(models.Model):
    created_date = models.DateField(auto_now=True)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    guest = models.ForeignKey(flight_models.User, on_delete=models.CASCADE)
    total_amount = models.IntegerField(default=0)
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=20, default="")
    status = models.CharField(max_length=45, choices=ORDER_STATUS, default='PENDING')

    ref_no = models.CharField(max_length=8, unique=True, blank=True)

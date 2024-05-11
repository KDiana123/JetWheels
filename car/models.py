from django.db import models

from flight import models as flight_models


# Create your models here.


class Car(models.Model):
    car_name = models.CharField(max_length=30, default="")
    car_desc = models.CharField(max_length=300, default="")
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="flight/static/car/images", default="")
    pickup_location = models.ForeignKey(flight_models.Place, on_delete=models.CASCADE, related_name="pickup_location")

    def __str__(self):
        return self.car_name


ORDER_STATUS =(
    ('PENDING', 'Pending'),
    ('PAID', 'Paid'),
    ('CONFIRMED', 'Confirmed'),
    ('CANCELLED', 'Cancelled'),
    ('CLOSED', 'Closed')
)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(flight_models.User, on_delete=models.CASCADE, related_name="orders")
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=20, default="")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="cars")
    pickup_date = models.DateField(blank=True, null=True)
    dropoff_date = models.DateField(blank=True, null=True)
    total_amount = models.IntegerField(default=0)
    status = models.CharField(max_length=45, choices=ORDER_STATUS, default='PENDING')
    ref_no = models.CharField(max_length=8, unique=True, blank=True)
from django.db import models

from flight import models as flight_models


# Create your models here.
class Hotels(models.Model):
    # h_id,h_name,owner ,location,rooms
    name = models.CharField(max_length=30, default="noname")
    owner = models.CharField(max_length=20)
    location = models.ForeignKey(flight_models.Place, on_delete=models.CASCADE, related_name="location")

    def __str__(self):
        return self.name


class Rooms(models.Model):
    ROOM_STATUS = (
        ("1", "available"),
        ("2", "not available"),
    )

    ROOM_TYPE = (
        ("1", "premium"),
        ("2", "deluxe"),
        ("3", "basic"),
    )

    # type,no_of_rooms,capacity,prices,Hotel
    room_type = models.CharField(max_length=50, choices=ROOM_TYPE)
    capacity = models.IntegerField()
    price = models.IntegerField()
    size = models.IntegerField()
    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE)
    status = models.CharField(choices=ROOM_STATUS, max_length=15)
    room_number = models.IntegerField()

    def __str__(self):
        return self.hotel.name


class Reservation(models.Model):
    check_in = models.DateField(auto_now=False)
    check_out = models.DateField()
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    guest = models.ForeignKey(flight_models.User, on_delete=models.CASCADE)

    booking_id = models.CharField(max_length=100, default="null")

    def __str__(self):
        return self.guest.username
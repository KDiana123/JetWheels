from django.contrib import admin

from tour.models import Tour, Reservation

# Register your models here.


class TourAdmin(admin.ModelAdmin):
    list_display = ('tour_name', 'start_date', 'end_date', 'price', 'tour_capacity', 'location')


admin.site.register(Tour, TourAdmin)
admin.site.register(Reservation)
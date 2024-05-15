from django.urls import path
from . import views

urlpatterns = [
    path("hotel", views.car_index, name="carindex"),
]
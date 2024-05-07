from django.urls import path
from . import views

urlpatterns = [
    path("cars", views.car_index, name="carindex"),
    path("cars/search", views.car, name="cars_search"),
    path("cars/review", views.review, name="car_review"),
]
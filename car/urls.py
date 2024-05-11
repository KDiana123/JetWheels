from django.urls import path
from . import views

urlpatterns = [
    path("cars", views.car_index, name="carindex"),
    path("cars/search", views.car, name="cars_search"),
    path("cars/review", views.review, name="car_review"),
    path("cars/book", views.book, name="car_book"),
    path("cars/payment", views.payment, name="car_payment"),
    path('cars/ticket/api/<str:ref>', views.ticket_data, name="ticketdata"),
    path('analytics/', views.dashboard, name='analytics'),
    path('cars/print', views.get_ticket, name="cargetticket"),
]
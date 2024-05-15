from django.urls import path
from . import views

urlpatterns = [
    path("tour", views.tour_index, name="tourindex"),
    path("tour/search", views.tour, name="tour_search"),
    path("tour/review", views.review, name="tour_review"),
    path("tour/book", views.book, name="tour_book"),
    path("tour/payment", views.payment, name="car_payment"),
    path('tour/ticket/api/<str:ref>', views.ticket_data, name="tourdata"),
    path('tour/print', views.get_ticket, name="tourgetticket"),
]
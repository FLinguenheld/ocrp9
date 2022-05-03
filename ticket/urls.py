from django.contrib import admin
from django.urls import path

# import views
from ticket import views

urlpatterns = [
    path('ticket/list/', views.list_tickets, name='ticket_list'),
    path('ticket/add/', views.add_ticket, name='ticket_add')
]

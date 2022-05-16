from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('ticket/add', views.CreateTicketView.as_view(), name='create_ticket'),
    path('ticket/<int:id>/update/', views.UpdateTicketView.as_view(), name='update_ticket')
]

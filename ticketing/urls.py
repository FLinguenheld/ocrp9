from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('ticket/add', views.CreateTicketView.as_view(), name='create_ticket'),
    path('ticket/<int:ticket_id>/update/', views.UpdateTicketView.as_view(), name='update_ticket'),
    path('ticket/<int:ticket_id>/delete/', views.DeleteTicketView.as_view(), name='delete_ticket'),
    path('ticket/<int:ticket_id>/add-review/', views.CreateReviewView.as_view(), name='create_review'),
]

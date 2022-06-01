from django.urls import path
from . import views

urlpatterns = [
    path('flux/', views.FluxView.as_view(), name='home'),
    path('flux_test/', views.FluxView_Test.as_view(), name='home_test'),
    path('posts/', views.PostView.as_view(), name='posts'),
    path('ticket/add', views.CreateTicketView.as_view(), name='create_ticket'),
    path('review/add', views.CreateCompleteReviewView.as_view(), name='create_complete_review'),
    path('ticket/<int:id>/update/', views.UpdateTicketView.as_view(), name='update_ticket'),
    path('ticket/<int:id>/delete/', views.DeleteTicketView.as_view(), name='delete_ticket'),
    path('ticket/<int:id>/add-review/', views.CreateReviewView.as_view(), name='create_review'),
    path('review/<int:id>/update/', views.UpdateReviewView.as_view(), name='update_review'),
    path('review/<int:id>/delete/', views.DeleteReviewView.as_view(), name='delete_review'),
]

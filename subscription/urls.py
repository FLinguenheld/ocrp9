from django.urls import path
from . import views


urlpatterns = [
    path('subscription-management/', views.SubscriptionManagementView.as_view(), name='subscription_management'),
]

from django.urls import path
from . import views

urlpatterns = [
    # path('home/', views.HomeView.as_view(), name='home'),
    path('subscription-management/', views.SubscriptionManagementView.as_view(), name='subscription_management'),
    path('subscription/<int:userfollows_id>/delete/', views.DeleteSubscriptionView.as_view(), name='delete_subscription'),
]

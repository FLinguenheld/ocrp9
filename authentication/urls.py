from django.urls import path
from django.contrib.auth.views import (LoginView,
                                       LogoutView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView)
from . import views

urlpatterns = [
    path('', LoginView.as_view(template_name='authentication/login.html',
                               redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('password-change/',
         PasswordChangeView.as_view(template_name='authentication/password_change_form.html'),
         name='password_change'),
    path('password-change-done/',
         PasswordChangeDoneView.as_view(template_name='authentication/password_change_done.html'),
         name='password_change_done'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('my-account/', views.MyAccountView.as_view(), name='my_account'),
    path('my-account/update/', views.UpdateAccountView.as_view(), name='update_account'),
    path('my-account/update/photo', views.UpdatePhotoView.as_view(), name='update_photo'),
]

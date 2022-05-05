from django.urls import path
from django.contrib.auth.views import (LoginView,
                                       LogoutView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView)
from authentication.views import SignupView


urlpatterns = [
    path('', LoginView.as_view(template_name='authentication/login.html',
                               redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('password-change/', PasswordChangeView.as_view(
                               template_name='authentication/password_change_form.html'),
                               name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(
                                    template_name='authentication/password_change_done.html'),
                                    name='password_change_done'),
    path('signup/', SignupView.as_view(), name='signup')
]

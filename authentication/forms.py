from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from . import models

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'photo')

class UpdateForm(ModelForm):
    class Meta():
        model = models.User
        fields = ('username', 'email', 'first_name', 'last_name', 'photo')

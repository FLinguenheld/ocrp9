from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from . import models

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')

class UpdateForm(ModelForm):
    class Meta():
        model = models.User
        fields = ('username', 'first_name', 'last_name', 'email')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['email'].widget.attrs.update({'class': 'bg-primary'})
    #     self.fields['username'].widget.attrs.update({'class': 'pouletttttt'})

class UpdatePhotoForm(ModelForm):
    class Meta():
        model = models.User
        fields = ['photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs.update({'class': 'p-1 m-2 border bg-light'})

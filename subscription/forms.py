from django.forms import ModelForm
from django import forms
from .models import UserFollows


class NewSubscriptionForm(ModelForm):
    new_sub = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta():
        model = UserFollows
        exclude = ['user']


class DeleteSubscriptionForm(ModelForm):
    delete_sub = forms.IntegerField(widget=forms.HiddenInput )

    class Meta():
        model = UserFollows
        # fields = '__all__'
        exclude = ['user', 'followed_user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['followed_user'].widget = forms.HiddenInput()

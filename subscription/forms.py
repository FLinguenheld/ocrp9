from django import forms


class RemoveSubscriptionForm(forms.Form):
    # delete_sub = forms.IntegerField(initial=True, disabled=True, required=False)
    delete_sub = forms.IntegerField(widget=forms.HiddenInput, initial=True)

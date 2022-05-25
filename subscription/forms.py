from django import forms


class RemoveSubscriptionForm(forms.Form):
    # delete_sub = forms.IntegerField(initial=True, disabled=True, required=False)
    delete_sub = forms.IntegerField(widget=forms.HiddenInput, initial=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

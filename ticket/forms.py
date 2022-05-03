from django import forms

from ticket.models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        # exclude = ('time_created')

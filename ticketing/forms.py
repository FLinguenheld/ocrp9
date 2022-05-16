from django.forms import ModelForm

from . import models


class TicketForm(ModelForm):
    class Meta():
        model = models.Ticket
        exclude = ('user', 'time_created')

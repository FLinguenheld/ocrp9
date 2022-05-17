from django.forms import ModelForm

from . import models


class TicketForm(ModelForm):
    class Meta():
        model = models.Ticket
        exclude = ('user', 'time_created', 'time_edited')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'w-100 h3 text-center',
                                                  'placeholder': 'Titre'})
        
        self.fields['description'].widget.attrs.update({'class': 'w-100 text-justify',
                                                        'placeholder': 'Description'})

class ReviewForm(ModelForm):
    class Meta():
        model = models.Review
        exclude = ('user', 'ticket', 'time_created', 'time_edited')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['headline'].widget.attrs.update({'class': 'w-100 h3 text-center',
                                                  'placeholder': 'Titre'})

        self.fields['body'].widget.attrs.update({'class': 'w-100 text-justify',
                                                  'placeholder': 'Critique'})

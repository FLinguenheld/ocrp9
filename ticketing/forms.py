from django.forms import ModelForm
from django.forms import RadioSelect, ChoiceField
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

    RATING = [(str(x), x) for x in range(0, 6)]
    rating_choice = ChoiceField(widget=RadioSelect(attrs={'class': 'form-check-input ml-2'}),
                                choices=RATING,
                                label='Note :')

    class Meta():
        model = models.Review
        fields = ('headline', 'rating_choice', 'body')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['headline'].widget.attrs.update({'class': 'w-100 h3 text-center',
                                                        'placeholder': 'Titre'})

        self.fields['body'].widget.attrs.update({'class': 'w-100 text-justify',
                                                  'placeholder': 'Critique'})

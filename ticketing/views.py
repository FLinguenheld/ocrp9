from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime

from . import forms
from .models import Ticket, Review


class HomeView(LoginRequiredMixin, View):
    template_name = 'ticketing/home.html'

    def get(self, request):

        # Lists all reviews with their tickets
        reviews = Review.objects.all()

        for review in reviews:
            ticket = Ticket.objects.filter(id=review.ticket.id)
            review.ticket_ooject = ticket.first()

            rating = review.rating
            review.rating = ['Y' for y in range(rating)]
            review.rating += ['N' for n in range(rating, 5)]  # How getting the max validator ?

        # lists all user's tikets
        tickets = Ticket.objects.all()
        for t in tickets:
            if Review.objects.filter(ticket=t.id):
                t.already_reviewed = True
            else:
                t.already_reviewed = False

        return render(request, self.template_name, context={'reviews': reviews,
                                                             'tickets': tickets})


class CreateCompleteReviewView(LoginRequiredMixin, View):
    template_name = 'ticketing/create_complete_review.html'
    title = "Création d'un ticket et de sa critique"

    def get(self, request):
        form_ticket = forms.TicketForm()
        form_review = forms.ReviewForm(initial={'rating_choice': 5})

        return render(request, self.template_name, context={'form_ticket': form_ticket,
                                                            'form_review': form_review,
                                                            'title': self.title,
                                                            'text_button': 'Créer et publier'})

    def post(self, request):
        form_ticket = forms.TicketForm(request.POST, request.FILES)
        form_review = forms.ReviewForm(request.POST, initial={'rating_choice': 5})

        if all([form_ticket.is_valid(), form_review.is_valid()]):
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = form_review.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.rating = form_review.cleaned_data.get('rating_choice')
            review.save()

            return redirect('home')

        else:
            return render(request, self.template_name, context={'form_ticket': form_ticket,
                                                                'form_review': form_review,
                                                                'title': self.title,
                                                                'text_button': 'Créer et publier'})


class CreateTicketView(LoginRequiredMixin, View):
    template_name = 'ticketing/create_ticket.html'
    title = 'Nouveau ticket'

    def get(self, request):
        form = forms.TicketForm()
        return render(request, self.template_name, context={'form_ticket': form,
                                                            'title': self.title,
                                                            'text_button': 'Créer'})

    def post(self, request):
        form = forms.TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            return redirect('home')

        else:
            return render(request, self.template_name, context={'form_ticket': form,
                                                                'title': self.title,
                                                                'text_button': 'Créer'})


class UpdateTicketView(LoginRequiredMixin, View):
    template_name = 'ticketing/create_ticket.html'
    title = 'Modification du ticket'

    def get(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        form = forms.TicketForm(instance=ticket)
        return render(request, self.template_name, context={'form_ticket': form,
                                                            'title': self.title,
                                                            'text_button': 'Modifier'})

    def post(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.time_edited = datetime.today()
            ticket.save()

            return redirect('home')

        else:
            return render(request, self.template_name, context={'form_ticket': form,
                                                                 'title': self.title,
                                                                 'text_button': 'Modifier'})


class DeleteTicketView(LoginRequiredMixin, View):
    template_name = 'ticketing/delete_ticket.html'

    def get(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        return render(request, self.template_name, context={'ticket': ticket})
    
    def post(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.delete()

        return redirect('home')


class CreateReviewView(LoginRequiredMixin, View):
    template_name = 'ticketing/create_review.html'
    title = "Écriture d'une critique"

    def get(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        form = forms.ReviewForm(initial={'rating_choice': 5})

        return render(request, self.template_name, context={'t': ticket,
                                                            'form_review': form,
                                                            'title': self.title,
                                                            'text_button': 'Publier'})

    def post(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        form = forms.ReviewForm(request.POST, initial={'rating_choice': 5})

        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.rating = form.cleaned_data.get('rating_choice')
            review.save()

            return redirect('home')

        else:
            return render(request, self.template_name, context={'t': ticket,
                                                                'form_review': form,
                                                                'title': self.title,
                                                                'text_button': 'Publier'})


class UpdateReviewView(LoginRequiredMixin, View):
    template_name = 'ticketing/create_review.html'
    title = "Modification d'une critique"

    def get(self, request, review_id):
        review = Review.objects.get(id=review_id)
        ticket = Ticket.objects.get(id=review.ticket.id)
        form = forms.ReviewForm(instance=review, initial={'rating_choice': review.rating})

        return render(request, self.template_name, context={'t': ticket,
                                                            'form_review': form,
                                                            'title': self.title,
                                                            'text_button': 'Modifier'})

    def post(self, request, review_id):
        review = Review.objects.get(id=review_id)
        ticket = Ticket.objects.get(id=review.ticket.id)
        form = forms.ReviewForm(request.POST, instance=review, initial={'rating_choice': review.rating})

        if form.is_valid():
            review = form.save(commit=False)
            review.time_edited = datetime.today()
            review.rating = form.cleaned_data.get('rating_choice')
            review.save()

            return redirect('home')

        else:
            return render(request, self.template_name, context={'t': ticket,
                                                                'form_review': form,
                                                                'title': self.title,
                                                                'text_button': 'Modifier'})
        

class DeleteReviewView(LoginRequiredMixin, View):
    template_name = 'ticketing/delete_review.html'

    def get(self, request, review_id):
        review = Review.objects.get(id=review_id)
        return render(request, self.template_name, context={'review': review})
    
    def post(self, request, review_id):
        review = Review.objects.get(id=review_id)
        review.delete()

        return redirect('home')

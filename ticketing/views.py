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

        # lists all user's tikets
        # tickets = Ticket.objects.filter(user=request.user)
        tickets = Ticket.objects.all()

        return render(request, self.template_name, context={'reviews': reviews,
                                                             'tickets': tickets})


class CreateTicketView(LoginRequiredMixin, View):
    template_name = 'ticketing/create_ticket.html'
    title = 'Nouveau ticket'

    def get(self, request):
        form = forms.TicketForm()
        return render(request, self.template_name, context={'form': form,
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
            return render(request, self.template_name, context={'form': form,
                                                                 'title': self.title,
                                                                 'text_button': 'Créer'})


class UpdateTicketView(LoginRequiredMixin, View):
    template_name = 'ticketing/create_ticket.html'
    title = 'Modification du ticket'

    def get(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        form = forms.TicketForm(instance=ticket)
        return render(request, self.template_name, context={'form': form,
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
            return render(request, self.template_name, context={'form': form,
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
        form = forms.ReviewForm()

        return render(request, self.template_name, context={'t': ticket,
                                                             'form': form,
                                                             'title': self.title,
                                                             'text_button': 'Publier'})

    def post(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        form = forms.ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            return redirect('home')

        else:
            return render(request, self.template_name, context={'t': ticket,
                                                                 'form': form,
                                                                 'title': self.title,
                                                                 'text_button': 'Publier'})


class UpdateReviewView(LoginRequiredMixin, View):
    template_name = 'ticketing/create_review.html'
    title = "Modification d'une critique"

    def get(self, request, review_id):
        review = Review.objects.get(id=review_id)
        ticket = Ticket.objects.get(id=review.ticket.id)
        form = forms.ReviewForm(instance=review)

        return render(request, self.template_name, context={'t': ticket,
                                                            'form': form,
                                                            'title': self.title,
                                                            'text_button': 'Modifier'})

    def post(self, request, review_id):
        review = Review.objects.get(id=review_id)
        ticket = Ticket.objects.get(id=review.ticket.id)
        form = forms.ReviewForm(request.POST, instance=review)

        if form.is_valid():
            review = form.save(commit=False)
            review.time_edited = datetime.today()
            review.save()

            return redirect('home')

        else:
            return render(request, self.template_name, context={'t': ticket,
                                                                'form': form,
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

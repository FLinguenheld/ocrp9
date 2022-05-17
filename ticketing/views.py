from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime

from . import forms
from .models import Ticket


class HomeView(LoginRequiredMixin, View):
    templapte_name = 'ticketing/home.html'

    def get(self, request):
        # tickets = Ticket.objects.all()
        tickets = Ticket.objects.filter(user=request.user)

        return render(request, self.templapte_name, context={'tickets': tickets})


class CreateTicketView(LoginRequiredMixin, View):
    templapte_name = 'ticketing/create_ticket.html'
    title = 'Nouveau ticket'

    def get(self, request):
        form = forms.TicketForm()
        return render(request, self.templapte_name, context={'form': form, 'title': self.title})

    def post(self, request):
        form = forms.TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            return redirect('home')

        else:
            return render(request, self.templapte_name, context={'form': form, 'title': self.title})


class UpdateTicketView(LoginRequiredMixin, View):
    templapte_name = 'ticketing/create_ticket.html'
    title = 'Modification du ticket'

    def get(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        form = forms.TicketForm(instance=ticket)
        return render(request, self.templapte_name, context={'form': form, 'title': self.title})


    def post(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.time_edited = datetime.today()
            ticket.save()

            return redirect('home')

        else:
            return render(request, self.templapte_name, context={'form': form, 'title': self.title})


class DeleteTicketView(LoginRequiredMixin, View):
    templapte_name = 'ticketing/delete_ticket.html'

    def get(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        return render(request, self.templapte_name, context={'ticket': ticket})
    
    def post(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.delete()

        return redirect('home')

class CreateReviewView(LoginRequiredMixin, View):
    templapte_name = 'ticketing/create_review.html'
    title = "Écriture d'une critique"

    def get(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        form = forms.ReviewForm()
        return render(request, self.templapte_name, context={'t': ticket, 'form': form, 'title': self.title})

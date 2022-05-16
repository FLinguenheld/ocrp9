from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

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

    def get(self, request):
        form = forms.TicketForm()
        return render(request, self.templapte_name, context={'form': form})

    def post(self, request):
        form = forms.TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            return redirect('home')
        else:
            return render(request, self.templapte_name, context={'form': form})

class UpdateTicketView(LoginRequiredMixin, View):
    templapte_name = 'ticketing/update_ticket.html'


    def get(self, request, ticket_id):
        # ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket = Ticket.objects.get(id=ticket_id)
        form = forms.TicketForm(instance=ticket)
        return render(request, self.templapte_name, context={'form': form})


    def post(self, request, ticket_id):
        # ticket = get_object_or_404(Ticket, id=id)
        ticket = Ticket.objects.get(id=ticket_id)
        form = forms.TicketForm(request.POST, instance=ticket)

        if form.is_valid():
            form.save()
            return redirect('home')

        else:
            return render(request, self.templapte_name, context={'form': form})

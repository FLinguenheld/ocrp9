from django.shortcuts import render, redirect

from ticket.models import Ticket
from ticket.forms import TicketForm


def list_tickets(request):

    tickets = Ticket.objects.all()
    return render(request, 'list.html', {'tickets': tickets})

def add_ticket(request):

    if request.method == 'POST':
        form = TicketForm(request.POST)

        if form.is_valid():
            
            form.save()
            return redirect('ticket_list')

    else:
        form = TicketForm()

    return render(request, 'add.html', {'form': TicketForm()})

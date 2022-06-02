from itertools import chain
import functools
from django.shortcuts import render, redirect

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models import CharField, Value

from django.utils.timezone import now

from . import forms
from .models import Ticket, Review
from subscription.models import UserFollows


def check_user(Model):
    """ Decorator used to check whether the user in request is the same that the user in the Model.get(id).user """

    def decorator_check_user(func):
        @functools.wraps(func)
        def wrapper_check_user(*args, **kwargs):

            try:
                if 'id' in kwargs and Model.objects.get(id=kwargs['id']).user == args[1].user:
                    return func(*args, **kwargs)
                else:
                    return redirect('home')

            except Model.DoesNotExist:
                return redirect('home')

        return wrapper_check_user
    return decorator_check_user


class CheckUserMixin():

    def check(self, request, id, Model):
        try:
            print('c est bon ?')
            if Model.objects.get(id=id).user == request.user:
                print('c est bon')
                return True
            else:
                print('baaaaaahhhhhhhhh ?')
                return redirect('home')

        except Model.DoesNotExist:
            return redirect('home')


class FluxView(LoginRequiredMixin, View):
    template_name = 'ticketing/flux.html'

    def get(self, request):

        followed_users = UserFollows.objects.filter(user=request.user).values('followed_user')

        # Get all tikets and reviews (mines and those of my followed users)
        # Then all reviews (+ reviews from tickets even if they aren't been written by us)
        # Then exclude tickets with review (to prevent doubles)
        tickets = Ticket.objects.filter(Q(user=request.user) | Q(user__in=followed_users))
        reviews = Review.objects.filter(Q(user=request.user) | Q(user__in=followed_users) | Q(ticket__in=tickets))
        tickets = tickets.exclude(review__in=reviews)

        # Add annotations to recognise them in templates
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        # Combine and sort the two types of posts
        posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

        return render(request, self.template_name, context={'posts': posts})


class PostView(LoginRequiredMixin, View):
    template_name = 'ticketing/post.html'

    def get(self, request):

        # For the post, tickets have to be display even if a review has been created (asked by specifications)
        # They will be display twice
        tickets = Ticket.objects.filter(user=request.user)
        reviews = Review.objects.filter(Q(user=request.user) | Q(ticket__in=tickets))

        # Add annotations to recognise them in templates
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        # Combine and sort the two types of posts
        posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

        return render(request, self.template_name, context={'posts': posts})


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


class UpdateTicketView(LoginRequiredMixin, View, CheckUserMixin):
    template_name = 'ticketing/create_ticket.html'
    title = 'Modification du ticket'

    # @check_user(Model=Ticket)
    def get(self, request, id):
        super().check(request=request, id=id, Model=Ticket)

        ticket = Ticket.objects.get(id=id)
        form = forms.TicketForm(instance=ticket)
        return render(request, self.template_name, context={'form_ticket': form,
                                                            'title': self.title,
                                                            'text_button': 'Modifier'})

    @check_user(Model=Ticket)
    def post(self, request, id):
        ticket = Ticket.objects.get(id=id)
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.time_edited = now()
            ticket.save()

            return redirect('posts')

        else:
            return render(request, self.template_name, context={'form_ticket': form,
                                                                 'title': self.title,
                                                                 'text_button': 'Modifier'})


class DeleteTicketView(LoginRequiredMixin, View):
    template_name = 'ticketing/delete_ticket.html'

    @check_user(Model=Ticket)
    def get(self, request, id):
        ticket = Ticket.objects.get(id=id)
        return render(request, self.template_name, context={'ticket': ticket})

    @check_user(Model=Ticket)
    def post(self, request, id):
        ticket = Ticket.objects.get(id=id)
        ticket.delete()

        return redirect('posts')


class CreateReviewView(LoginRequiredMixin, View):
    template_name = 'ticketing/create_review.html'
    title = "Écriture d'une critique"

    def get(self, request, id):
        ticket = Ticket.objects.get(id=id)
        form = forms.ReviewForm(initial={'rating_choice': 5})

        return render(request, self.template_name, context={'t': ticket,
                                                            'form_review': form,
                                                            'title': self.title,
                                                            'text_button': 'Publier'})

    def post(self, request, id):
        ticket = Ticket.objects.get(id=id)
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

    @check_user(Model=Review)
    def get(self, request, id):
        review = Review.objects.get(id=id)
        ticket = Ticket.objects.get(id=review.ticket.id)
        form = forms.ReviewForm(instance=review, initial={'rating_choice': review.rating})

        return render(request, self.template_name, context={'t': ticket,
                                                            'form_review': form,
                                                            'title': self.title,
                                                            'text_button': 'Modifier'})

    @check_user(Model=Review)
    def post(self, request, id):
        review = Review.objects.get(id=id)
        ticket = Ticket.objects.get(id=review.ticket.id)
        form = forms.ReviewForm(request.POST, instance=review, initial={'rating_choice': review.rating})

        if form.is_valid():
            review = form.save(commit=False)
            review.time_edited = now()
            review.rating = form.cleaned_data.get('rating_choice')
            review.save()

            return redirect('posts')

        else:
            return render(request, self.template_name, context={'t': ticket,
                                                                'form_review': form,
                                                                'title': self.title,
                                                                'text_button': 'Modifier'})


class DeleteReviewView(LoginRequiredMixin, View):
    template_name = 'ticketing/delete_review.html'

    @check_user(Model=Review)
    def get(self, request, id):
        review = Review.objects.get(id=id)
        return render(request, self.template_name, context={'review': review})

    @check_user(Model=Review)
    def post(self, request, id):
        review = Review.objects.get(id=id)
        review.delete()

        return redirect('posts')

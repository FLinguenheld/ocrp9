from django.shortcuts import render, redirect

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms
from .models import UserFollows


class SubscriptionManagementView(LoginRequiredMixin, View):
    template_name = 'subscription/management.html'

    def get(self, request):

        subscriptions = {}
        for user in UserFollows.objects.filter(user=request.user.id):
            subscriptions[user.followed_user] = user.id

        # sort ???

        return render(request, self.template_name, context={'subscriptions': subscriptions})




    def post(self, request):

        forms_unsubscribe = forms.DeleteSubscriptionForm(request.POST)

        if forms_unsubscribe.is_valid():
            return redirect('home')

        else:
            print('prOut de mammouth')
            return render(request, self.template_name, context={'forms_unsubscribe': forms_unsubscribe})


class DeleteSubscriptionView(LoginRequiredMixin, View):

    def get(self, request, userfollows_id):
        subscription = UserFollows.objects.get(id=userfollows_id)
        subscription.delete()

        return redirect('subscription_management')

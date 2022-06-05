from django.shortcuts import render, redirect

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms
from .models import UserFollows
from authentication.models import User


class SubscriptionManagementView(LoginRequiredMixin, View):
    template_name = 'subscription/management.html'

    def get(self, request):

        # Get active subscriptons for delete forms and to skip it in new subscription list
        already_followed = []
        active_subscriptions = {}
        for sub in UserFollows.objects.filter(user=request.user.id):
            active_subscriptions[sub.followed_user] = forms.RemoveSubscriptionForm(initial={'delete_sub': sub.id})
            already_followed.append(sub.followed_user)

        # Choice list -> Form created directly in the template
        choices = {}
        for user in User.objects.all():
            if user not in already_followed and user.username != 'admin' and user.username != request.user.username:
                choices[user.username] = user.id

        active_followers = []
        for sub in UserFollows.objects.filter(followed_user=request.user.id):
            active_followers.append(sub.user)

        # Sort needed ?
        return render(request, self.template_name, context={'choices': choices,
                                                            'subscriptions': active_subscriptions,
                                                            'followers': active_followers})

    def post(self, request):

        if 'delete_sub' in request.POST:
            forms_unsubscribe = forms.RemoveSubscriptionForm(request.POST)

            if forms_unsubscribe.is_valid():

                UserFollows.objects.get(id=forms_unsubscribe.cleaned_data['delete_sub']).delete()
                return redirect('subscription_management')

            else:
                return render(request, self.template_name)

        elif 'new_subscription' in request.POST:

            print(request.POST.get('new_subscription'))
            followed_user = User.objects.get(id=request.POST.get('new_subscription'))

            new_entry = UserFollows()
            new_entry.user = request.user
            new_entry.followed_user = followed_user
            new_entry.save()

            return redirect('subscription_management')

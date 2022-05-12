from django.shortcuts import render
from django.views.generic import View

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render

import os

from . import forms

class SignupView(View):
    template_name = 'authentication/signup.html'
    
    def get(self, request):
        form = forms.SignupForm()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = forms.SignupForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

        return render(request, self.template_name, context={'form': form})

class MyAccountView(LoginRequiredMixin, View):
    template_name = 'authentication/my_account.html'

    def get(self, request):
        return render(request, self.template_name)

class UpdateAccountView(LoginRequiredMixin, View):
    template_name = 'authentication/update_account.html'

    def get(self, request):
        form = forms.UpdateForm(instance=request.user)
        return render(request, self.template_name, context={'form': form})
    
    def post(self, request):
        form = forms.UpdateForm(request.POST, request.FILES, instance=request.user)
        # request.user.photo.delete()

        if form.is_valid():
            form.save()
            
            return redirect('home')
        else:
            return render(request, self.template_name, context={'form': form})
        

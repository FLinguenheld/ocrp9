from django.shortcuts import render
from django.views.generic import View

from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render

from . import forms

class SignupView(View):
    template_name = 'authentication/signup.html'
    form_class = forms.SignupForm

    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

        return render(request, self.template_name, context={'form': form})

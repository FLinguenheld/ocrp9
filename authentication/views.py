from django.conf import settings
from django.shortcuts import redirect, render

from django.views.generic import View
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

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
        form = forms.UpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            
            return redirect('my_account')
        else:
            return render(request, self.template_name, context={'form': form})

class UpdatePhotoView(LoginRequiredMixin, View):
    template_name = 'authentication/update_photo.html'

    def get(self, request):
        form = forms.UpdatePhotoForm(instance=request.user)
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = forms.UpdatePhotoForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            user = form.save()
            user.resize_photo()

            return redirect('my_account')
        else:
            return render(request, self.template_name, context={'form': form})

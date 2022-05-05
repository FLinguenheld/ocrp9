from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin



class HomeView(LoginRequiredMixin, View):
    template_name = 'ticket/home.html'
    
    def get(self, request):
        return render(request, self.template_name)


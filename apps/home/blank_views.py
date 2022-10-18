from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.home.models import *
from apps.home.forms import UrlBaseForm

from django.urls import reverse, reverse_lazy

class BlankView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'   
    template_name = 'home/blank.html'    
    model = UrlBase
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        obj = UrlBase.objects.all().filter(user=self.request.user).first()        
        context['obj'] = obj
        return context
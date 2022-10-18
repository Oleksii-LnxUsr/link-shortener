from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.home.models import *
from apps.home.forms import UrlBaseForm

from django.urls import reverse, reverse_lazy

class MainView(LoginRequiredMixin, ListView):
    #login_url = '/accounts/login/'   
    login_url = 'login'   
    template_name = 'home/main.html'    
    model = UrlBase
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        #org = Org.objects.all().filter(user=self.request.user).first()
        #context['org'] = org
        #context['sheduler'] = Sheduler.objects.all().filter(org=org)
        return context
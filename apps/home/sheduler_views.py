from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.home.models import *
from apps.home.forms import *

from django.urls import reverse, reverse_lazy

class ShedulerListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'    
    template_name = 'home/sheduler/list.html'    
    model = Sheduler
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        org = Org.objects.all().filter(user=self.request.user).first()
        context['org'] = org
        context['sheduler'] = Sheduler.objects.all().filter(org=org)
        return context


class ShedulerCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    template_name = 'home/sheduler/add.html'
    model = Sheduler
    form_class = ShedulerForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        org = Org.objects.all().filter(user=self.request.user).first()
        context['org'] = org
        context['sheduler'] = Sheduler.objects.all().filter(org=org)
        return context
        
    def get_initial(self):
        initial = super().get_initial()
        initial['org'] = Org.objects.all().filter(user=self.request.user).first()
        return initial
        
    def get_success_url(self, *args):
        #messages.success(self.request, f"Новость  {self.object.name}  создано !")
        return reverse('sheduler_add')

class ShedulerUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    template_name = 'home/sheduler/edit.html'
    model = Sheduler
    form_class = ShedulerForm
    
    def get_success_url(self, *args):        
        return reverse('sheduler_add')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        org = Org.objects.all().filter(user=self.request.user).first()
        context['org'] = org        
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        initial['org'] = Org.objects.all().filter(user=self.request.user).first()
        return initial

class ShedulerDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = Sheduler
    
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        #messages.success(self.request, f"Удалено !")
        return reverse('sheduler_add')
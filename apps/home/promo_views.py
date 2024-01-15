from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.home.models import *
from apps.home.forms import PromoForm
from django.urls import reverse, reverse_lazy

import random

RANDOM_STRING = "ABCEHKMPTX0123456789"
ITEM_RANDOM_CHAR = 6



def getRandom(count_random):
    strRandom = ""
    for i in range(count_random):
        strRandom = strRandom + random.choice(RANDOM_STRING)
        obj_search = Promo.objects.all().filter(stringPromo=RANDOM_STRING).first()
        if obj_search!=None:
            while obj_search!=None:
                count_random = count_random + 1
                strRandom = getRandom(count_random)
                obj_search = Promo.objects.all().filter(stringPromo=RANDOM_STRING).first()
    return strRandom
    


class PromoView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    template_name = 'home/promo/list.html'
    paginate_by = 50
    model = Promo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objs'] = Promo.objects.all()
        return context



class PromoCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    template_name = 'home/promo/add.html'
    model = Promo 
    form_class = PromoForm
        
    def get_initial(self):        
        initial = super().get_initial()
        initial['stringPromo'] = getRandom(ITEM_RANDOM_CHAR)        
        return initial
        
    def get_success_url(self, *args):
        return reverse('promo_list')
        
    def form_valid(self, form):
        errors = {}
        self.object = form.save(commit=False)
        self.object.save()
        
        return super().form_valid(form)

class PromoUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    template_name = 'home/promo/edit.html'
    model = Promo 
    form_class = PromoForm
        
    def get_success_url(self, *args):
        return reverse('promo_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_id'] = self.object.pk
        return context
        
    def form_valid(self, form):
        errors = {}
        self.object = form.save(commit=False)
        self.object.save()
        
        return super().form_valid(form)

class PromoDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = Promo    
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    def get_success_url(self):        
        return reverse('promo_list')
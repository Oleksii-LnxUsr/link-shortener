from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.home.models import *
from apps.home.forms import UrlBaseForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect

import random
import segno


RANDOM_STRING = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
ITEM_RANDOM_CHAR = 4

def getRandom(count_random):
    strRandom = ""
    for i in range(count_random):
        strRandom = strRandom + random.choice(RANDOM_STRING)
        obj_search = UrlBase.objects.all().filter(shortUrl=RANDOM_STRING).first()
        if obj_search!=None:
            while obj_search!=None:
                count_random = count_random + 1
                strRandom = getRandom(count_random)
                obj_search = UrlBase.objects.all().filter(shortUrl=RANDOM_STRING).first()
    return strRandom


class MainView(ListView):
    #login_url = '/accounts/login/'   
    #login_url = 'login'   
    template_name = 'home/main.html'    
    model = UrlBase

class MainCreateView(CreateView):
    #login_url = '/accounts/login/'
    template_name = 'home/main/add.html'
    model = UrlBase 
    form_class = UrlBaseForm
        
    def get_success_url(self, *args):
        
        return reverse('url_view',  kwargs={'pk': self.object.pk})
        
    def form_valid(self, form):
        errors = {}
        self.object = form.save(commit=False)
        self.object.shortUrl = "https://okqr.ru/"+getRandom(ITEM_RANDOM_CHAR)
        self.object.typeSource = 'www'
        self.object.save()
        
        return super().form_valid(form)

class MainUpdateView(UpdateView):    
    template_name = 'home/main/edit.html'
    model = UrlBase
    form_class = UrlBaseForm

    def get_success_url(self, *args):        
        return reverse('blank')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        short_url = self.object.shortUrl
        qrcode = segno.make(short_url, error='Q')
        file_name='apps/static/assets/img/'+short_url.replace('https://okqr.ru/','')+'.svg'
        qrcode.save(file_name, scale=4)
        svg_data  = ''
        with open(file_name,'r')as file:
            svg_data = file.read().replace('<?xml version="1.0" encoding="utf-8"?>\n', '')
        print('file_name->',file_name)
        context['svg_data'] = svg_data
        context['svg_file'] = short_url.replace('https://okqr.ru/','')+'.svg'
        
        
        context['short_url'] = short_url
        return context
    
    def form_valid(self, form):
        errors = {}
        self.object = form.save(commit=False)
        self.object.save()
        
        return super().form_valid(form)
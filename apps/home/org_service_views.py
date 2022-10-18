from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.home.models import *
from apps.home.forms import OrgServiceForm

from django.urls import reverse, reverse_lazy

class OrgServiceListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    paginate_by = 50
    template_name = 'home/org_service/list.html'
    #context_object_name = 'org_services'
    model = OrgService
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        org = Org.objects.all().filter(user=self.request.user).first()
        context['org'] = org
        context['main'] = OrgService.objects.all().filter(org=org)
        return context


class OrgServiceCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    template_name = 'home/org_service/add.html'
    model = OrgService
    form_class = OrgServiceForm    

    def get_success_url(self, *args):        
        return reverse('org_service_list')
    
    def get_initial(self):
        org = Org.objects.all().filter(user=self.request.user).first()        
        return { 'org': org.id }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        org = Org.objects.all().filter(user=self.request.user).first()        
        context['org'] = org        
        context['main'] = OrgService.objects.all().filter(org=org)
        return context

class OrgServiceUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    template_name = 'home/org_service/edit.html'
    model = OrgService
    form_class = OrgServiceForm
    #context_key = 'org_service_edit'

    def get_success_url(self, *args):        
        return reverse('org_service_list')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        org = Org.objects.all().filter(user=self.request.user).first()
        context['org'] = org        
        return context

class OrgServiceDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = OrgService    
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    def get_success_url(self):        
        return reverse('org_service_list')
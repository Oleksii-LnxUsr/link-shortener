from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.home.models import *
from apps.home.forms import OrgFieldTemplateForm

from django.urls import reverse, reverse_lazy

class OrgFieldTemplateListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    paginate_by = 50
    template_name = 'home/org_field_template/list.html'
    #context_object_name = 'org_field_template'
    model = OrgFieldTemplate
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        org = Org.objects.all().filter(user=self.request.user).first()
        context['org'] = org
        context['org_field_template'] = OrgFieldTemplate.objects.all().filter(org=org)
        return context

class OrgFieldTemplateCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    template_name = 'home/org_field_template/add.html'
    model = OrgFieldTemplate
    form_class = OrgFieldTemplateForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        org = Org.objects.all().filter(user=self.request.user).first()
        context['org'] = org        
        return context
        
    def get_initial(self):
        org = Org.objects.all().filter(user=self.request.user).first()
        return { 'org': org.id }

    def get_success_url(self, *args):        
        return reverse('org_field_template_list')

class OrgFieldTemplateUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    template_name = 'home/org_field_template/edit.html'
    model = OrgFieldTemplate
    form_class = OrgFieldTemplateForm    

    def get_success_url(self, *args):        
        return reverse('org_field_template_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        org = Org.objects.all().filter(user=self.request.user).first()
        context['org'] = org        
        return context


class OrgFieldTemplateDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = OrgFieldTemplate    
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    def get_success_url(self):
        #messages.success(self.request, f"Удалено !")
        return reverse('org_field_template_list')
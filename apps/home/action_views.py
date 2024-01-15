from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.home.models import *
from apps.home.forms import ActionForm
from django.urls import reverse, reverse_lazy

class ActionView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    template_name = 'home/action/list.html'
    paginate_by = 50
    model = Action
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        #org = Org.objects.all().filter(user=self.request.user).first()
        #context['org'] = org
        context['actions'] = Action.objects.all()
        return context

class ActionCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    template_name = 'home/action/add.html'
    model = Action 
    form_class = ActionForm
        
    def get_success_url(self, *args):
        return reverse('action_list')
        
    def form_valid(self, form):
        errors = {}
        self.object = form.save(commit=False)
        self.object.save()
        
        return super().form_valid(form)

class ActionUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    template_name = 'home/action/edit.html'
    model = Action 
    form_class = ActionForm
        
    def get_success_url(self, *args):
        return reverse('action_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_id'] = self.object.pk
        return context
        
    def form_valid(self, form):
        errors = {}
        self.object = form.save(commit=False)
        self.object.save()
        
        return super().form_valid(form)

class ActionDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = Action    
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    def get_success_url(self):        
        return reverse('action_list')
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.home.models import *
from apps.home.forms import OrgForm

from django.urls import reverse, reverse_lazy

from apps.home.tasks import send_feedback_bot_task

class OrgListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    paginate_by = 50
    template_name = 'home/org/org_list.html'
    context_object_name = 'orgs'
    model = Org
    #+++    
    #extra_context = {'rulesAdminMenu': RulesAdminMenu.objects.all().filter(pk=4).first()}
    #---
   
    '''
    def get(self, request, *args, **kwargs):
        
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form

        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        #print('user->', self.request.user)
        queryset = super().get_queryset()
        
        if self.search_value:
            query = Q(name__icontains=self.search_value) | Q(text__icontains=self.search_value) | \
                    Q(nameEN__icontains=self.search_value) | Q(textEN__icontains=self.search_value)

            queryset = queryset.filter(query)
        queryset = queryset.filter(type_of_affiliationV2='Региональные новости').order_by('-dateUpd')
        
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None
    '''

class OrgCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    template_name = 'home/org/org_add.html'
    model = Org
    form_class = OrgForm    

    def get_success_url(self, *args):        
        return reverse('main')


class OrgUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    template_name = 'home/org/org_edit.html'
    model = Org
    form_class = OrgForm
    #context_key = 'org'

    def get_success_url(self, *args):
        #messages.success(self.request, f"Новость  {self.object.name}  создано !")
        #send_feedback_bot_task.delay(self.object.id)
        
        return reverse('main')


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.home.models import *
from apps.home.forms import OrgWorkersForm

from django.urls import reverse, reverse_lazy

class OrgWorkersListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    paginate_by = 50
    template_name = 'home/org_workers/list.html'
    #context_object_name = 'org_workers'
    model = OrgWorkers
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        org = Org.objects.all().filter(user=self.request.user).first()
        context['org'] = org
        context['org_workers'] = OrgWorkers.objects.all().filter(org=org)
        return context


class OrgWorkersCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    template_name = 'home/org_workers/add.html'
    model = OrgWorkers
    form_class = OrgWorkersForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        org = Org.objects.all().filter(user=self.request.user).first()
        context['org'] = org        
        services = OrgService.objects.all().filter(org=org)
        context['services'] = services
        return context
    
    def get_initial(self):
        org = Org.objects.all().filter(user=self.request.user).first()
        #user = self.request.user
        #return { 'org': org, 'user' : self.request.user}
        return { 'org': org.id}
        
    def get_success_url(self, *args):        
        return reverse('org_workers_list')
        
    def form_valid(self, form):        
        errors = {}                
        self.object = form.save(commit=False)                
        self.object.save()        
        for k,v in self.request.POST.items():
            if 'id_s_k_' not in k:
                continue
            else:                
                id = k[len('id_s_k_'):len(k)]                
                #for k1,v1 in self.request.POST.items():
                    #if (k1 != 'id_s_v_'+str(id)):
                    #    continue
                    #else:
                        
                        #o_s = OrgService.objects.all().filter(pk = int(id)).first()
                        #OrgWorkersOrgService.objects.create(org_workers = self.object, org_service = o_s, k = float(v1))
                o_s = OrgService.objects.all().filter(pk = int(id)).first()
                OrgWorkersOrgService.objects.create(org_workers = self.object, org_service = o_s, k = float(1.00))
        return super().form_valid(form)

class OrgWorkersUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    template_name = 'home/org_workers/edit.html'
    model = OrgWorkers
    form_class = OrgWorkersForm

    def get_success_url(self, *args):        
        return reverse('org_workers_list')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        org = Org.objects.all().filter(user=self.request.user).first()
        context['org'] = org        
        services = OrgService.objects.all().filter(org=org).values()
        for s in services:
            print('s',s)
            o_w_s_find = OrgWorkersOrgService.objects.all().filter(org_workers = self.get_object()).filter(org_service__pk = s['id']).first()
            if o_w_s_find!=None:
                s['its_check'] = True
                s['its_value'] = o_w_s_find.k
                #s['its_value'] = 1.00
        context['services'] = services
        return context
    
    def form_valid(self, form):
        errors = {}
        self.object = form.save(commit=False)
        self.object.save()
        o_w_s = OrgWorkersOrgService.objects.all().filter(org_workers = self.object)
        for w in o_w_s:
            w.delete()
        for k,v in self.request.POST.items():
            if 'id_s_k_' not in k:
                continue
            else:                
                id = k[len('id_s_k_'):len(k)]
                #for k1,v1 in self.request.POST.items():
                    #if (k1 != 'id_s_v_'+str(id)):
                    #    continue
                    #else:
                    #    o_s = OrgService.objects.all().filter(pk = int(id)) .first()
                        #OrgWorkersOrgService.objects.create(org_workers = self.object, org_service = o_s, k = float(v1))
                    #    OrgWorkersOrgService.objects.create(org_workers = self.object, org_service = o_s, k = float(1.00))
                o_s = OrgService.objects.all().filter(pk = int(id)) .first()
                OrgWorkersOrgService.objects.create(org_workers = self.object, org_service = o_s, k = float(1.00))
                        
        return super().form_valid(form)

class OrgWorkersDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    model = OrgWorkers    
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    def get_success_url(self):        
        return reverse('org_workers_list')
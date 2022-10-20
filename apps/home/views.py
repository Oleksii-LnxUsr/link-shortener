# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponsePermanentRedirect
from django.template import loader
from django.urls import reverse

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from apps.home.models import *

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import datetime
import random


RANDOM_STRING = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
ITEM_RANDOM_CHAR = 4


def redirect_url(request, short_url):
    print('short_url->',short_url)
    find_obj = UrlBase.objects.all().filter(shortUrl = 'https://okqr.ru/'+short_url).first()
    if find_obj!=None:
        return HttpResponsePermanentRedirect(find_obj.longUrl)
    else:
        context = {'error_url': 'https://okqr.ru/'+short_url}
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))


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


class UrlBaseView(APIView):
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]
    def post(self, request):
        postData = json.dumps(request.data)
        jsonData = json.loads(postData)
        print('jsonData->',jsonData)        
        l_result = []
        for v in jsonData:
            obj = UrlBase.objects.create()
            obj.longUrl = v['url']
            print('v->',v['url'])
            obj.shortUrl = "https://okqr.ru/"+getRandom(ITEM_RANDOM_CHAR)
            obj.typeSource = 'api'
            obj.save()
            l_result.append({'longUrl':obj.longUrl, 'shortUrl':obj.shortUrl})
        return JsonResponse({"result": list(l_result)}, safe=False)


'''    
@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    #except:
    #    html_template = loader.get_template('home/page-500.html')
    #    return HttpResponse(html_template.render(context, request))

def get_token(request, pk):
    org = Org.objects.all().filter(id=pk).first()
    if org!=None:
        return JsonResponse({'token': org.t_token}, safe=False)
    else:
        return JsonResponse({'token': None}, safe=False)

def get_hello_phrases(request, pk):
    org = Org.objects.all().filter(id=pk).first()
    if org!=None:
        return JsonResponse({'hello_phrases': org.t_start_phrases}, safe=False)
    else:
        return JsonResponse({'hello_phrases': None}, safe=False)

def get_org_note(request, pk):
    org = Org.objects.all().filter(id=pk).first()
    if org!=None:
        return JsonResponse({'note_text': org.note_text}, safe=False)
    else:
        return JsonResponse({'note_text': None}, safe=False)

def get_w(request, pk):
    org = Org.objects.all().filter(id=pk).first()
    w__id = OrgWorkersOrgService.objects.all().filter(org_workers__org=org).filter(org_workers__moderation=True).values('org_workers__id').distinct()    
    w = OrgWorkers.objects.all().filter(org=org).filter(pk__in=w__id).values('id','name').distinct()
    return JsonResponse({'w': list(w)}, safe=False)

def get_params(request, pk):
    org = Org.objects.all().filter(id=pk).first()
    return JsonResponse({'its_name': org.its_name, 'its_phone': org.its_phone, 'its_email': org.its_email}, safe=False)    


def get_s(request, org_id, w_id):
    org = Org.objects.all().filter(id=org_id).first()    
    w = OrgWorkers.objects.all().filter(id=w_id).first()
    service__id = OrgWorkersOrgService.objects.all().filter(org_workers=w).values('org_service__id').distinct()
    s = OrgService.objects.all().filter(org=org).filter(pk__in = service__id).values('id','name').distinct()
    return JsonResponse({'s': list(s)}, safe=False)

def get_free_time(request, w_id, d_string):
    w = OrgWorkers.objects.all().filter(id=w_id).first()
    
    #13_00
    #2022_09_10
    
    h_start = int(w.org.datetime_string_start.split(":")[0])
    h_end = int(w.org.datetime_string_end.split(":")[0])
    today = datetime.datetime.today()
    
    its_today = False
    if (today.strftime("%Y_%m_%d"))==d_string:
        its_today = True
    print('its_today-->>',its_today)
    array_h=[]    
    for i in range(h_start,h_end):
        s_h = ''
        if (i>=0 and i<=9):
            s_h = '0'+str(i)+':00'
        else:
            s_h = str(i)+':00'
        sheduler = Sheduler.objects.all().filter(org_workers = w).filter(h_string = s_h.replace(':','_')).filter(d_string = d_string).first()        
        print('today.hour + 2-->>',today.hour)
        print('i-->>',i)
        if sheduler==None:
            if its_today and i>=(today.hour):                
                array_h.append(s_h)
            elif its_today==False:
                array_h.append(s_h)
    print('array_h-->',array_h)
    
    return JsonResponse({'array_h': array_h}, safe=False)


def get_user_session_param(request, org_id, user_id):
    sheduler = Sheduler.objects.all().filter(user_id = user_id).order_by('-pk').first()
    t_user = {}
    if (sheduler!=None):
        t_user = {'username_input': sheduler.username_input, 'phone_input': sheduler.phone_input, 'email_input': sheduler.email_input}    
    print('t_user-->',t_user)
    
    return JsonResponse({'t_user': t_user}, safe=False)


class ShedulerView(APIView):
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]
    def post(self, request):
        postData = json.dumps(request.data)
        jsonData = json.loads(postData)
        print('jsonData->',jsonData)
        #PriceUpd.objects.all().delete()
        with open('sheduler.txt', 'w') as f:
            json.dump(jsonData, f, ensure_ascii=False)
        for k,v in jsonData.items():            
            #print('k-->',k)
            #print('v-->',v)
            #print('data-->',)
            #{'data': {'w_id': 10, 's_id': 14, 'd': '2022_09_10', 'h': '15_00', 't_user_id': 203261079}}
            org_workers = OrgWorkers.objects.all().filter(pk = int(v['data']['w_id'])).first()
            if org_workers!=None:
                org = org_workers.org
            org_service = OrgService.objects.all().filter(pk = int(v['data']['s_id'])).first()
            d_string = v['data']['d']
            h_string = v['data']['h']
            user_id = v['data']['t_user_id']
            username_input = v['data']['username_input']
            phone_input = v['data']['phone_input']
            email_input = v['data']['email_input']
            if org_workers!=None and org!=None and org_service!=None:
                #d[8:11]+'.'+d[5:7]+'.'+d[0:4]
                d_datetime = datetime.datetime(int(d_string[0:4]), int(d_string[5:7]), int(d_string[8:11]), int(h_string.split("_")[0]), int(h_string.split("_")[1]))
                sh = Sheduler.objects.create(org = org, org_workers = org_workers, org_service = org_service, d_string = d_string, h_string = h_string,user_id = user_id, d_datetime = d_datetime, 
                                             username_input = username_input, phone_input = phone_input, email_input = email_input)
                return JsonResponse({"result": "ok"}, safe=False)
            else:
                return HttpResponseNotFound("error data")
        
'''
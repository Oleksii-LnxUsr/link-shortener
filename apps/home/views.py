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

from django.http import Http404
from django.conf import settings
import os.path
import segno

RANDOM_STRING = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
ITEM_RANDOM_CHAR = 4


def redirect_url(request, short_url):
    print('short_url->',short_url)
    find_obj = UrlBase.objects.all().filter(shortUrl = 'https://okqr.ru/'+short_url).first()
    if find_obj!=None:
        find_obj.count = find_obj.count + 1
        print('find_obj.count->',find_obj.count)
        find_obj.save()
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

class UrlBaseOneView(APIView):
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]
    def get(self, request, short_url):
        find_obj = UrlBase.objects.all().filter(shortUrl = 'https://okqr.ru/'+short_url).first()
        if find_obj!=None:
            path_file_save = os.path.join(settings.MEDIA_ROOT, 'QR',short_url+'.svg')
            print('path_file_save-->', path_file_save)
            path_file_obj = os.path.join('QR',short_url+'.svg')
            
            qrcode = segno.make(find_obj.shortUrl, error='Q')
            qrcode.save(path_file_save, scale=4)
            find_obj.img_svg.name = path_file_obj
            find_obj.count = find_obj.count + 1
            find_obj.save()
            l_result = {'id':find_obj.id, 'longUrl':find_obj.longUrl, 'shortUrl':find_obj.shortUrl, 'img_svg': find_obj.img_svg.url }
            return JsonResponse(l_result, safe=False)
        else:
            raise Http404
    def post(self, request):
        postData = json.dumps(request.data)
        jsonData = json.loads(postData)
        print('jsonData->',jsonData)        
        v = jsonData
        obj = UrlBase.objects.create()
        obj.longUrl = v['longUrl']
        print('v->',v['longUrl'])
        obj.shortUrl = "https://okqr.ru/"+getRandom(ITEM_RANDOM_CHAR)
        obj.typeSource = 'api'
        obj.save()
        l_result = {'id':obj.id, 'longUrl':obj.longUrl, 'shortUrl':obj.shortUrl}
        return JsonResponse(l_result, safe=False)

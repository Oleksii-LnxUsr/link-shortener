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

from user_agents import parse
from django.contrib.auth.models import User, Group 

import qrcode
import qrcode.image.svg

#from django.contrib.gis.geoip2 import GeoIP2


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

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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
            
            #qrcode = segno.make(find_obj.shortUrl, error='Q')
            #qrcode.save(path_file_save, scale=4)
            #qr = qrcode.QRCode(
            #    version=1,
            #    error_correction=qrcode.constants.ERROR_CORRECT_Q,
            #    box_size=10,
            #    border=4,
            #)
            #qr.add_data(find_obj.shortUrl)            
            #qr.make(fit=True)            
            #img = qr.make_image(fill_color="black", back_color="white")
            factory = qrcode.image.svg.SvgPathImage
            img = qrcode.make(find_obj.shortUrl, image_factory=factory)
            img.save(path_file_save)
            find_obj.img_svg.name = path_file_obj
            find_obj.count = find_obj.count + 1
            find_obj.save()
            
            userIP = get_client_ip(request)
            agent = request.META['HTTP_USER_AGENT']
            user_agent = parse(agent)
            
            typeDevice = 'none'
            
            if user_agent.is_mobile:
                typeDevice = 'mobile'
            elif user_agent.is_tablet:
                typeDevice = 'tablet'
            elif user_agent.is_pc:
                typeDevice = 'pc'
                
            UserInfo.objects.create(urlBase = find_obj, lastUrl = '', shortUrl = find_obj.shortUrl, typeDevice = typeDevice,  userIP = userIP)
            
            l_result = {'id':find_obj.id, 'longUrl':find_obj.longUrl, 'shortUrl':find_obj.shortUrl, 'img_svg': find_obj.img_svg.url, 'ip_user': find_obj.userIP}
            return JsonResponse(l_result, safe=False)
        else:
            raise Http404
    def post(self, request):
        postData = json.dumps(request.data)
        jsonData = json.loads(postData)
        #print('jsonData->',jsonData)        
        v = jsonData
        obj = UrlBase.objects.create()
        obj.longUrl = v['longUrl']
        #print('v->',v['longUrl'])
        shortCode = getRandom(ITEM_RANDOM_CHAR)
        obj.shortUrl = "https://okqr.ru/"+ shortCode
        obj.typeSource = 'www'
        #
        path_file_save = os.path.join(settings.MEDIA_ROOT, 'QR',shortCode+'.svg')
        print('path_file_save-->', path_file_save)
        path_file_obj = os.path.join('QR',shortCode+'.svg')
        qrcode = segno.make(obj.shortUrl, error='Q')
        qrcode.save(path_file_save, scale=4, lineclass=None, omitsize=True)
        obj.img_svg.name = path_file_obj
        
        ip_user = get_client_ip(request)
        obj.userIP = ip_user
        
        agent = request.META['HTTP_USER_AGENT']
        user_agent = parse(agent)
        # Определяем мобильное устройство
        print(user_agent.device)
        # Определяем производителя
        print(user_agent.device.brand)
        # Операционная система
        print(user_agent.os)
        # Семейство операционной системы
        print(user_agent.os.family)
        # Тип браузера
        print(user_agent.browser)
        # Версия
        print(user_agent.browser.version)        
        # Мобильный клиент
        print('user_agent.is_mobile',user_agent.is_mobile)
        # Планшет
        print('user_agent.is_tablet',user_agent.is_tablet)
        # Поддерживает касание
        print('user_agent.is_touch_capable',user_agent.is_touch_capable)
        # ПК        
        print('user_agent.is_pc',user_agent.is_pc)
        # Поисковый бот        
        print('user_agent.is_bot',user_agent.is_bot)
        
        if user_agent.is_mobile:
            obj.typeDevice = 'mobile'
        elif user_agent.is_tablet:
            obj.typeDevice = 'tablet'
        elif user_agent.is_pc:
            obj.typeDevice = 'pc'
        else:
            obj.typeDevice = 'none'
            
        #
        obj.save()
        l_result = {'id':obj.id, 'longUrl':obj.longUrl, 'shortUrl':obj.shortUrl, 'img_svg':obj.img_svg.url}
        return JsonResponse(l_result, safe=False)



def add_temp_user(request):
    #g = GeoIP2()
    #print('META->',request.META)
    agent = request.META['HTTP_USER_AGENT']
    user_agent = parse(agent)
    # Определяем мобильное устройство
    print(user_agent.device)
    # Определяем производителя
    print(user_agent.device.brand)
    # Операционная система
    print(user_agent.os)
    # Семейство операционной системы
    print(user_agent.os.family)
    # Тип браузера
    print(user_agent.browser)
    # Версия
    print(user_agent.browser.version)        
    # Мобильный клиент
    print('user_agent.is_mobile',user_agent.is_mobile)
    # Планшет
    print('user_agent.is_tablet',user_agent.is_tablet)
    # Поддерживает касание
    print('user_agent.is_touch_capable',user_agent.is_touch_capable)
    # ПК        
    print('user_agent.is_pc',user_agent.is_pc)
    # Поисковый бот        
    print('user_agent.is_bot',user_agent.is_bot)
    ip_user = get_client_ip(request)
    shortCode = getRandom(ITEM_RANDOM_CHAR)
    u_obj = User.objects.create_user(shortCode.lower(),
                                     email=shortCode.lower()+'@tempuser.com',
                                         password=shortCode)
    result = {'username':shortCode.lower(), 'password': shortCode}
    return JsonResponse(result, safe=False)
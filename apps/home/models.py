# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User, Group 

# Create your models here.


class UrlBase(models.Model):
    TYPE_SOURCE = (
        ('www', 'www'),
        ('api', 'api'),
    )
    
    TYPE_DEVICE = (
        ('none', 'none'),
        ('mobile', 'mobile'),
        ('tablet', 'tablet'),
        ('pc', 'pc'),
    )
    
    user = models.ForeignKey(User,models.SET_NULL,blank=True,null=True, verbose_name='Пользователь')
    longUrl = models.CharField(max_length=2083, blank=True, null=True, verbose_name="Исходная ссылка")
    shortUrl = models.CharField(max_length=255, blank=True, null=True, verbose_name="Короткая сслылка")
    count = models.IntegerField(default = 0, verbose_name='Количество открытий')
    img_svg = models.FileField(upload_to='QR', null=True, blank=True, verbose_name='QR')
    
    typeSource = models.CharField(
            max_length=10,
            choices=TYPE_SOURCE,
            default='www',
            verbose_name='Источник',
            null=True, blank=True
        )
    
    typeDevice = models.CharField(
            max_length=10,
            choices=TYPE_DEVICE,
            default='none',
            verbose_name='Тип устройства',
            null=True, blank=True
        )
    userIP = models.CharField(max_length=50, blank=True, null=True, verbose_name="IP")

    updated_at = models.DateTimeField(verbose_name='updated date', auto_now=True)
    created_at = models.DateTimeField(verbose_name='created date', auto_now_add=True, null=True)
    
    def __str__(self):
        return self.longUrl.__str__() 
        
    class Meta:
        verbose_name = 'Ссылки'
        verbose_name_plural = 'Ссылки'
        
        
class UserInfo(models.Model):
    TYPE_DEVICE = (
        ('none', 'none'),
        ('mobile', 'mobile'),
        ('tablet', 'tablet'),
        ('pc', 'pc'),
    )
    urlBase = models.ForeignKey(UrlBase,models.SET_NULL,blank=True,null=True, verbose_name='Url')
    lastUrl = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Источник перехода")
    shortUrl = models.CharField(max_length=255, blank=True, null=True, verbose_name="Короткая сслылка")
    user = models.ForeignKey(User,models.SET_NULL,blank=True,null=True, verbose_name='Пользователь')
    typeDevice = models.CharField(
            max_length=10,
            choices=TYPE_DEVICE,
            default='none',
            verbose_name='Тип устройства',
            null=True, blank=True
        )
    userIP = models.CharField(max_length=50, blank=True, null=True, verbose_name="IP")
    updated_at = models.DateTimeField(verbose_name='updated date', auto_now=True)
    
    
    def __str__(self):
        return self.shortUrl.__str__() + '__' + self.userIP.__str__() 
        
    class Meta:
        verbose_name = 'Сессии'
        verbose_name_plural = 'Сессии'
        
        

class Action(models.Model):
    shortDescription = models.CharField(max_length=255, blank=True, null=True, verbose_name="Короткое описание")
    itsOn = models.BooleanField(default=False, verbose_name='Активна')
    dateStart = models.DateTimeField(verbose_name='Дата начала', null=True, blank=True)
    dateEnd = models.DateTimeField(verbose_name='Дата окончания', null=True, blank=True)
    countPoint = models.IntegerField(default = 0, verbose_name='Количество баллов')
    dateEndPoint = models.DateTimeField(verbose_name='Срок действия баллов', null=True, blank=True)
    limitCountOn = models.IntegerField(default = 0, verbose_name='Максимальное число активаций')
    emailZone = models.CharField(max_length=255, blank=True, null=True, verbose_name="Email зона")
    updated_at = models.DateTimeField(verbose_name='updated date', auto_now=True)
    
    def __str__(self):
        return self.shortDescription.__str__() 
        
    class Meta:
        verbose_name = 'Акции'
        verbose_name_plural = 'Акции'

class Promo(models.Model):
    action = models.ForeignKey(Action,models.SET_NULL,blank=True,null=True, verbose_name='Акция')
    stringPromo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Строчка промо")
    itsOn = models.BooleanField(default=False, verbose_name='Активен')
    dateStart = models.DateTimeField(verbose_name='Дата создания', auto_now=True)
    dateEnd = models.DateTimeField(verbose_name='Срок действия', null=True, blank=True)
    limitCountOn = models.IntegerField(default = 0, verbose_name='Максимальное число активаций')
    currentCountOn = models.IntegerField(default = 0, verbose_name='Текущее число активаций')
    email = models.CharField(max_length=255, blank=True, null=True, verbose_name="email")

    updated_at = models.DateTimeField(verbose_name='updated date', auto_now=True)
    
    def __str__(self):
        return self.stringPromo.__str__() 
        
    class Meta:
        verbose_name = 'ПромоКоды'
        verbose_name_plural = 'ПромоКоды'

class PromoOnList(models.Model):
    promo = models.ForeignKey(Promo,models.SET_NULL,blank=True,null=True, verbose_name='ПромоКод')
    stringPromo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Строчка промо")
    phone = models.CharField(max_length=255, blank=True, null=True, verbose_name="телефон")    
    dateOn = models.DateTimeField(verbose_name='Дата активации', auto_now=True)
    
    updated_at = models.DateTimeField(verbose_name='updated date', auto_now=True)
    
    def __str__(self):
        return self.stringPromo.__str__()  + '_' + self.phone.__str__()
        
    class Meta:
        verbose_name = 'ПромоКодыАктивация'
        verbose_name_plural = 'ПромоКодыАктивация'
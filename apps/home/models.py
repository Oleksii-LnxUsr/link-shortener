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
    user = models.ForeignKey(User,models.SET_NULL,blank=True,null=True, verbose_name='Пользователь')
    longUrl = models.CharField(max_length=255, blank=True, null=True, verbose_name="Исходная ссылка")
    shortUrl = models.CharField(max_length=255, blank=True, null=True, verbose_name="Короткая сслылка")
    count = models.IntegerField(default = 0, verbose_name='Количество открытий')

    typeSource = models.CharField(
            max_length=10,
            choices=TYPE_SOURCE,
            default='www',
            verbose_name='Источник',
            null=True, blank=True
        )
        
    updated_at = models.DateTimeField(verbose_name='updated date', auto_now=True)
    
    
    def __str__(self):
        return self.longUrl.__str__() 
        
    class Meta:
        verbose_name = 'Ссылки'
        verbose_name_plural = 'Ссылки'
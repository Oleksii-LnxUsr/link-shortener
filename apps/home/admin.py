# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import *

class UrlBaseAdmin(admin.ModelAdmin):
    list_display = ('longUrl','user', 'shortUrl', 'updated_at', 'typeSource')
admin.site.register(UrlBase, UrlBaseAdmin)
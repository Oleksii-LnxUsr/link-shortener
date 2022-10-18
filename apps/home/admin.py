# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import *

class UrlBaseAdmin(admin.ModelAdmin):
    list_display = ('user','shortUrl', 'longUrl')
admin.site.register(UrlBase, UrlBaseAdmin)
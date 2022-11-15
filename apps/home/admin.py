# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import *

class UrlBaseAdmin(admin.ModelAdmin):
    def url(self, obj):
        return u"%s..." % (obj.longUrl[:50],)
        
    list_display = ('url','user', 'shortUrl', 'updated_at', 'typeSource', 'count','typeDevice','userIP')
    list_filter = ('typeSource',)
    search_fields = ('shortUrl',)
    list_max_show_all = 1000
    list_per_page = 50

admin.site.register(UrlBase, UrlBaseAdmin)
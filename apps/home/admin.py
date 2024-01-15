# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import *

class UrlBaseAdmin(admin.ModelAdmin):
    def url(self, obj):
        if obj.longUrl!=None:
            return u"%s..." % (obj.longUrl[:50],)
        else:
            return "..."
        
    list_display = ('url','user', 'shortUrl', 'updated_at', 'created_at', 'typeSource', 'count','typeDevice','userIP')
    list_filter = ('typeSource',)
    search_fields = ('shortUrl','longUrl')
    list_max_show_all = 1000
    list_per_page = 50
    
admin.site.register(UrlBase, UrlBaseAdmin)

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('shortUrl', 'typeDevice','userIP')
    list_filter = ('shortUrl',)
    search_fields = ('shortUrl',)
    list_max_show_all = 1000
    list_per_page = 50

admin.site.register(UserInfo, UserInfoAdmin)

'''
class ActionAdmin(admin.ModelAdmin):
    list_display = ('shortDescription', 'itsOn','countPoint', 'dateStart', 'dateEnd')
    list_filter = ('itsOn','emailZone')
    search_fields = ('shortDescription',)
    list_max_show_all = 1000
    list_per_page = 50

admin.site.register(Action, ActionAdmin)

class PromoAdmin(admin.ModelAdmin):
    list_display = ('stringPromo', 'action','itsOn', 'dateStart', 'limitCountOn', 'currentCountOn', 'email')
    list_filter = ('itsOn','email')
    search_fields = ('stringPromo',)
    list_max_show_all = 1000
    list_per_page = 50

admin.site.register(Promo, PromoAdmin)

class PromoOnListAdmin(admin.ModelAdmin):
    list_display = ('stringPromo', 'phone','dateOn')
    list_filter = ('promo',)
    search_fields = ('shortDescription',)
    list_max_show_all = 1000
    list_per_page = 50

admin.site.register(PromoOnList, PromoOnListAdmin)


class OrgAdmin(admin.ModelAdmin):
    list_display = ('name')

admin.site.register(Org, OrgAdmin)

'''
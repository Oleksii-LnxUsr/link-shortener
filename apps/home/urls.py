# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from apps.home.blank_views import *
from apps.home.main_views import *
#from apps.home.org_views import *
#from apps.home.org_service_views import *
#from apps.home.org_workers_views import *
#from apps.home.org_field_template_views import *
#from apps.home.sheduler_views import *

from apps.home.views import  *




urlpatterns = [

    # The home page
    #path('', views.index, name='home'),
    #re_path(r'^/(?P<short_url>{})$', views.redirect_url, name='redirect_url'),
    #re_path(r'^/([A-Z])$', views.redirect_url, name='redirect_url'),
    #re_path(r'^(?P<short_url>\w+)$', views.redirect_url, name='redirect_url'),
    #re_path(r'(?P<short_url>\w{4,7})/$', views.redirect_url, name='redirect_url'),
    re_path(r'api/grs/(?P<short_url>\w{4,7})/$', UrlBaseOneView.as_view(), name='get_qr'),
    #path('<short_url>BZ2D', views.redirect_url, name='redirect_url'),   
    #path('', MainCreateView.as_view(), name='main_add'),
    path('url/<int:pk>/view/', MainUpdateView.as_view(), name='url_view'),
    
    #re_path('news_detail/(?P<news_id>[0-9]+)/$', views.news_detail, name='news_detail'),
    
    #path('', ShedulerCreateView.as_view(), name="main"),
    
    #path("blank/", BlankView.as_view(), name="blank"),
    path('api_v1/get_urls/', UrlBaseView.as_view(), name="get_urls"),
    path('api/grs', UrlBaseOneView.as_view(), name="api_grs_upd"),
]

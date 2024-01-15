# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
#from apps.home.blank_views import *
from apps.home.main_views import *
from apps.home.action_views import *
from apps.home.promo_views import *
#from apps.home.org_views import *
#from apps.home.org_service_views import *
#from apps.home.org_workers_views import *
#from apps.home.org_field_template_views import *
#from apps.home.sheduler_views import *

from apps.home.views import  *




urlpatterns = [
    re_path(r'api/grs/(?P<short_url>\w{4,7})/$', UrlBaseOneView.as_view(), name='get_qr'),
    path('url/<int:pk>/view/', MainUpdateView.as_view(), name='url_view'),    
    path('api_v1/get_urls/', UrlBaseView.as_view(), name="get_urls"),
    path('api/grs', UrlBaseOneView.as_view(), name="api_grs_upd"),
    path('api/add_temp_user', views.add_temp_user, name="add_temp_user"),
    path('back/action_list/', ActionView.as_view(), name='action_list'),
    path('back/action_add', ActionCreateView.as_view(), name='action_add'),
    path('back/action/<int:pk>/edit/', ActionUpdateView.as_view(), name='action_edit'),
    path('back/action/<int:pk>/delete/', ActionDeleteView.as_view(), name='action_delete'),
    path('back/promo_list/', PromoView.as_view(), name='promo_list'),
    path('back/promo_add', PromoCreateView.as_view(), name='promo_add'),
    path('back/promo/<int:pk>/edit/', PromoUpdateView.as_view(), name='promo_edit'),
    path('back/promo/<int:pk>/delete/', PromoDeleteView.as_view(), name='promo_delete'),
]

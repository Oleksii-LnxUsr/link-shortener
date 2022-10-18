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
    path('', MainView.as_view(), name='main'),
    #path('', ShedulerCreateView.as_view(), name="main"),
    
    path("blank/", BlankView.as_view(), name="blank"),
    
]

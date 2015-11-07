# -*- coding: utf-8 -*-
from django.conf.urls import include, url

from ui import views as ui_views


urlpatterns = [
    url(r'^$', ui_views.home, name='home'),
    url(r'^auth/', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^bank/', include('bank.urls', namespace='bank')),
]

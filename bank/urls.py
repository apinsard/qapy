# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.DashboardView.as_view(), name='index'),

    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),

    url(r'^accounts/$', views.AccountsView.as_view(), name='accounts'),
    url(r'^accounts/new/$', views.AccountCreateView.as_view(),
        name='accounts_new'),

    url(r'^boxes/$', views.BoxesView.as_view(), name='boxes'),
    url(r'^boxes/new/$', views.BoxCreateView.as_view(), name='boxes_new'),

    url(r'^transactions/$', views.TransactionsView.as_view(),
        name='transactions'),
    url(r'^transactions/new/$', views.TransactionCreateView.as_view(),
        name='transactions_new'),
]

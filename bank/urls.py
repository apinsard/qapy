# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.DashboardView.as_view(), name='index'),

    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),

    url(r'^accounts/$', views.AccountsView.as_view(), name='accounts'),
    url(r'^accounts/new/$', views.AccountCreateView.as_view(),
        name='accounts_new'),
    url(r'^accounts/(?P<pk>[0-9]+)/$',
        views.AccountUpdateView.as_view(),
        name='accounts_item'),
    url(r'^accounts/(?P<pk>[0-9]+)/delete/$',
        views.AccountDeleteView.as_view(),
        name='accounts_item_delete'),

    url(r'^boxes/$', views.BoxesView.as_view(), name='boxes'),
    url(r'^boxes/new/$', views.BoxCreateView.as_view(), name='boxes_new'),
    url(r'^boxes/(?P<pk>[0-9]+)/$', views.BoxUpdateView.as_view(),
        name='boxes_item'),
    url(r'^boxes/(?P<pk>[0-9]+)/delete/$', views.BoxDeleteView.as_view(),
        name='boxes_item_delete'),

    url(r'^transactions/$', views.TransactionsView.as_view(),
        name='transactions'),
    url(r'^transactions/new/$', views.TransactionCreateView.as_view(),
        name='transactions_new'),
    url(r'^transactions/(?P<pk>[0-9]+)/$',
        views.TransactionUpdateView.as_view(),
        name='transactions_item'),
    url(r'^transactions/(?P<pk>[0-9]+)/delete/$',
        views.TransactionDeleteView.as_view(),
        name='transactions_item_delete'),
]

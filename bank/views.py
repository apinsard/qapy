# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .models import Account, Box, Transaction


class DashboardView(View):
    pass


class AccountsView(ListView):
    model = Account


class AccountCreateView(CreateView):
    model = Account
    fields = ['name', 'amount', 'iban', 'bic', 'is_virtual']
    success_url = reverse_lazy('bank:accounts')
    template_name = 'bank/account_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class AccountUpdateView(View):
    model = Account


class BoxesView(ListView):
    model = Box


class BoxCreateView(CreateView):
    model = Box
    fields = ['name', 'short_description', 'amount', 'value', 'parent_box']
    success_url = reverse_lazy('bank:boxes')
    template_name = 'bank/box_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class BoxUpdateView(View):
    model = Box


class TransactionsView(View):
    model = Transaction


class TransactionCreateView(View):
    model = Transaction


class TransactionUpdateView(View):
    model = Transaction

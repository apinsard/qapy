# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.list import ListView

from .forms import TransactionCreateForm
from .models import Account, Box, Transaction


class DashboardView(TemplateView):
    template_name = 'bank/dashboard.html'


class AccountsView(ListView):
    model = Account

    def get_queryset(self):
        return self.model.objects.filter(owner_id=self.request.user.pk)


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


class AccountUpdateView(UpdateView):
    model = Account


class BoxesView(ListView):
    model = Box

    def get_queryset(self):
        return self.model.objects.filter(owner_id=self.request.user.pk)


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


class BoxUpdateView(UpdateView):
    model = Box


class TransactionsView(ListView):
    model = Transaction

    def get_queryset(self):
        return self.model.objects.filter(
            account__owner_id=self.request.user.pk)


class TransactionCreateView(FormView):
    form_class = TransactionCreateForm
    success_url = reverse_lazy('bank:transactions')
    template_name = 'bank/transaction_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['owner_id'] = self.request.user.pk
        return kwargs

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class TransactionUpdateView(UpdateView):
    model = Transaction

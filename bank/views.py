# -*- coding: utf-8 -*-
from datetime import datetime
from itertools import groupby

from django.core.urlresolvers import reverse_lazy
from django.db.models import Sum, F, Func
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import (
    FormView, CreateView, UpdateView, DeleteView,
)
from django.views.generic.list import ListView

from .forms import TransactionCreateForm, BoxTransferForm
from .models import Account, Box, Transaction


def _week_keyfunc(x):
    dt = x.date
    if format(dt, '%W') == '00':
        dt = datetime(dt.year-1, 12, 31)
    return format(dt, '%Y-%W')


class DashboardView(TemplateView):
    template_name = 'bank/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = Account.objects.filter(owner_id=self.request.user.pk)
        queryset = queryset.aggregate(total=Sum('amount'))
        amount = total_amount = queryset['total']

        transactions = Transaction.objects.filter(
            account__owner_id=self.request.user.pk).order_by('-date')

        by_weeks_keys = []
        by_weeks_values = []
        for k, v in groupby(transactions, _week_keyfunc):
            by_weeks_keys.append(k.split('-')[1])
            by_weeks_values.append(str(amount))
            amount -= sum(x.amount for x in v)

        by_months_keys = []
        by_months_values = []
        for k, v in groupby(transactions, lambda x: format(x.date, "%Y-%m")):
            by_months_keys.append(k.split('-')[1])
            by_months_values.append(str(sum(x.amount for x in v)))

        graph_weekly = {
            'keys': '[{}]'.format(','.join(by_weeks_keys[::-1])),
            'values': '[{}]'.format(','.join(by_weeks_values[::-1])),
        }

        graph_monthly = {
            'keys': '[{}]'.format(','.join(by_months_keys[::-1])),
            'values': '[{}]'.format(','.join(by_months_values[::-1])),
        }
        context['graph_weekly'] = graph_weekly
        context['graph_monthly'] = graph_monthly
        return context


class AccountsView(ListView):
    model = Account

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_amount'] = self.get_queryset().aggregate(
            total=Sum('amount'))['total']
        return context

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
    fields = ['name', 'amount', 'iban', 'bic', 'is_virtual']
    success_url = reverse_lazy('bank:accounts')
    template_name = 'bank/account_update.html'


class AccountDeleteView(DeleteView):
    model = Account
    success_url = reverse_lazy('bank:accounts')
    template_name = 'bank/account_delete.html'


class BoxesView(FormView):
    model = Box
    form_class = BoxTransferForm
    success_url = reverse_lazy('bank:boxes')
    template_name = 'bank/box_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.get_queryset()
        return context

    def get_queryset(self):
        return self.model.objects.filter(owner_id=self.request.user.pk)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())


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
    fields = ['name', 'short_description', 'amount', 'value', 'parent_box']
    success_url = reverse_lazy('bank:boxes')
    template_name = 'bank/box_update.html'


class BoxDeleteView(DeleteView):
    model = Box
    success_url = reverse_lazy('bank:boxes')
    template_name = 'bank/box_delete.html'


class TransactionsView(ListView):
    model = Transaction
    paginate_by = 30
    paginate_orphans = 10

    def get_queryset(self):
        return self.model.objects.filter(
            account__owner_id=self.request.user.pk).order_by('-date')


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
    fields = ['other', 'date', 'short_description']
    success_url = reverse_lazy('bank:transactions')
    template_name = 'bank/transaction_update.html'


class TransactionDeleteView(DeleteView):
    model = Transaction
    success_url = reverse_lazy('bank:transactions')
    template_name = 'bank/transaction_delete.html'

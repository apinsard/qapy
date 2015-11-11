# -*- coding: utf-8 -*-
from django import forms
from django.utils import timezone

from .models import Account, Box, Transaction, BoxTransfer

class TransactionCreateForm(forms.Form):
    from_account = forms.ModelChoiceField(queryset=Account.objects.none(),
                                          required=False)
    from_other = forms.CharField(max_length=50, required=False)
    amount = forms.DecimalField(max_digits=13, decimal_places=2)
    to_account = forms.ModelChoiceField(queryset=Account.objects.none(),
                                        required=False)
    to_other = forms.CharField(max_length=50, required=False)
    box = forms.ModelChoiceField(queryset=Box.objects.none())
    date = forms.DateField(initial=timezone.now)
    short_description = forms.CharField(max_length=100, required=False)

    def __init__(self, owner_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        account_queryset = Account.objects.filter(owner_id=owner_id)
        self.fields['from_account'].queryset = account_queryset
        self.fields['to_account'].queryset = account_queryset
        self.fields['box'].queryset = Box.objects.filter(owner_id=owner_id)
        if 'initial' not in kwargs or 'box' not in kwargs['initial']:
            self.fields['box'].initial = \
                self.fields['box'].queryset.get(name="Flow Box")

    def clean(self):
        cleaned_data = super().clean()
        from_account = cleaned_data.get('from_account')
        from_other = cleaned_data.get('from_other')
        to_account = cleaned_data.get('to_account')
        to_other = cleaned_data.get('to_other')

        if not from_account and not from_other:
            raise forms.ValidationError(_("You must specify the debitor."))
        elif from_account and from_other:
            raise forms.ValidationError(
                _("You must specify only one debitor."))

        if not to_account and not to_other:
            raise forms.ValidationError(_("You must specify the creditor."))
        elif to_account and to_other:
            raise forms.ValidationError(
                _("You must specify only one creditor."))

        if not from_account and not to_account:
            raise forms.ValidationError(_(
                "At least one of the debitor and the creditor must be one of "
                "your accounts"))
        elif from_account and to_account and from_account.pk == to_account.pk:
            raise forms.ValidationError(_(
                "You can't transfer money from one account to itself."))

        return cleaned_data

    def save(self):
        from_account = self.cleaned_data.get('from_account')
        from_other = self.cleaned_data.get('from_other')
        to_account = self.cleaned_data.get('to_account')
        to_other = self.cleaned_data.get('to_other')
        box = self.cleaned_data.get('box')
        date = self.cleaned_data.get('date')
        short_description = self.cleaned_data.get('short_description')
        amount = self.cleaned_data.get('amount')

        if from_account:
            Transaction.debits.create(account=from_account, box=box,
                                      other=(to_account or to_other),
                                      date=date, amount=amount,
                                      short_description=short_description)
        if to_account:
            Transaction.credits.create(account=to_account, box=box,
                                       other=(from_account or from_other),
                                       date=date, amount=amount,
                                       short_description=short_description)


class BoxTransferForm(forms.ModelForm):

    class Meta:
        model = BoxTransfer
        fields = ['from_box', 'to_box', 'amount']

    def save(self, commit=True):
        instance = super().save(commit=commit)
        instance.from_box.debit(instance.amount)
        instance.to_box.credit(instance.amount)
        if commit:
            instance.from_box.save()
            instance.to_box.save()
        return instance

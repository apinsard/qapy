# -*- coding: utf-8 -*-
from django.db import models


class TransactionManager(models.Manager):
    pass


class CreditManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(amount__gt=0)

    def create(self, account, box, other, amount, **kwargs):
        credit = self.model(account=account, box=box, other=str(other),
                           amount=abs(amount), **kwargs)
        account.credit(abs(amount))
        account.save()
        box.credit(abs(amount))
        box.save()
        credit.save()
        return credit


class DebitManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(amount__lt=0)

    def create(self, account, box, other, amount, **kwargs):
        debit = self.model(account=account, box=box, other=str(other),
                           amount=-abs(amount), **kwargs)
        account.debit(abs(amount))
        account.save()
        box.debit(abs(amount))
        box.save()
        debit.save()
        return debit

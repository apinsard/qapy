# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Account(models.Model):
    """Represent a container of money the user ownes.
    It can be either a bank account, a wallet, a moneybox or something less
    concrete such as lent money.
    In the latter case, the account is said "virtual", which means it is taken
    into account in the total amount of money of the user, though he doesn't
    actually have the money and is not guaranteed to get it back.
    """

    class Meta:
        verbose_name = _("account")
        verbose_name_plural = _("accounts")
        unique_together = [('owner', 'name')]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("owner"),
        related_name='accounts')
    name = models.CharField(verbose_name=_("name"), max_length=30)
    amount = models.DecimalField(
        verbose_name=_("amount"), max_digits=13, decimal_places=2)
    iban = models.CharField(verbose_name=_("IBAN"), max_length=34, blank=True)
    bic = models.CharField(verbose_name=_("BIC"), max_length=11, blank=True)
    is_virtual = models.BooleanField(
        verbose_name=_("virtual account"), default=False, help_text=_(
            "A virtual account is useful to keep track of money you own, "
            "though you don't actually have it. (Eg: money you lent)"))

    def __str__(self):
        owner_name = self.owner.get_full_name()
        if not owner_name:
            owner_name = self.owner.username
        return "{} - {}".format(self.name, owner_name)

    def credit(self, amount):
        """Credit the account of the given amount."""
        assert amount > 0
        self.amount = F('amount') + amount

    def debit(self, amount):
        """Debit the account of the given amount."""
        assert amount > 0
        self.amount = F('amount') - amount


class Box(models.Model):
    """Boxes enable the user to organize his money with respect to the way he
    spends it. It is a way to budget expenses.
    Every user has a default box called "Flow Box", which is not editable and
    which purpose is to be a transit box through which all transactions are
    made before affecting money to the right box. For instance, when you get
    you wage, it will be affected to the Flow Box. Then you will allocate some
    of the money to your "Bills Box", to your "Monthly Extra Box", to your
    "Yearly Extra Box", to your "Placement Box", ...
    This box is especially useful for incoming money. When you pay your rent
    for instance, you would rather affect the transaction directly to your
    "Bills Box".
    """

    class Meta:
        verbose_name = _("box")
        verbose_name_plural = _("boxes")
        unique_together = [('owner', 'name')]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("owner"),
        related_name='boxes')
    name = models.CharField(verbose_name=_("name"), max_length=30, unique=True)
    short_description = models.CharField(
        verbose_name=_("short description"), max_length=100)
    amount = models.DecimalField(
        verbose_name=_("amount"), max_digits=13, decimal_places=2)
    value = models.BigIntegerField(
        verbose_name=_("value"), blank=True, null=True, help_text=_(
            "This can be useful to set the expected value when the box is "
            "\"full\" or a goal to reach. This is not a limit, it only serves "
            "as an indication."),
        validators=[
            MinValueValidator(1),  # 0 would cause issues when calculating the
                                   # filling rate.
        ])
    parent_box = models.ForeignKey(
        'self', verbose_name=_("parent box"), related_name='subboxes',
        blank=True, null=True)

    def __str__(self):
        owner_name = self.owner.get_full_name()
        if not owner_name:
            owner_name = self.owner.username
        return "{} - {}".format(self.name, owner_name)


class Transaction(models.Model):
    """Represent a transaction which is crediting or debiting an account."""

    class Meta:
        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")

    account = models.ForeignKey(
        Account, verbose_name=_("account"), related_name='transactions',
        help_text=_("The account involved in the transaction."))
    box = models.ForeignKey(
        Box, verbose_name=_("box"), related_name='transactions',
        help_text=_("The box involved in the transaction."))
    other = models.CharField(
        verbose_name=_("other account"), max_length=50, help_text=_(
            "The name of the other account involved in the transaction."))
    amount = models.DecimalField(
        verbose_name=_("transaction amount"), max_digits=13, decimal_places=2)
    date = models.DateField(
        verbose_name=_("transaction date"), default=timezone.now)
    short_description = models.CharField(
        verbose_name=_("short_description"), max_length=100, blank=True)

    def __str__(self):
        if self.amount < 0:
            return "{date}: {account} > {amount}€ > {other} " % {
                'date': self.date,
                'account': self.account,
                'amount': abs(self.amount),
                'other': self.other
            }
        else:
            return "{date}: {account} < {amount}€ < {other} " % {
                'date': self.date,
                'account': self.account,
                'amount': abs(self.amount),
                'other': self.other
            }


class BoxTransfer(models.Model):
    """Represent a tranfer of money from a box to another."""

    class Meta:
        verbose_name = _("box transfer")
        verbose_name_plural = _("box transfers")

    from_box = models.ForeignKey(
        Box, verbose_name=_("debtor box"), related_name='debits')
    to_box = models.ForeignKey(
        Box, verbose_name=_("creditor box"), related_name='credits')
    amount = models.DecimalField(
        verbose_name=_("amount"), max_digits=13, decimal_places=2,
        validators=[
            MinValueValidator(0),
        ])
    date = models.DateField(
        verbose_name=_("transaction date"), default=timezone.now)

    def __str__(self):
        return "{date}: {from} > {amount}€ > {to} " % {
            'date': self.date,
            'from': self.from_box,
            'amount': abs(self.amount),
            'to': self.to_box
        }

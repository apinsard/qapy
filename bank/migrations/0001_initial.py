# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('amount', models.DecimalField(decimal_places=2, verbose_name='amount', max_digits=13)),
                ('iban', models.CharField(blank=True, max_length=34, verbose_name='IBAN')),
                ('bic', models.CharField(blank=True, max_length=11, verbose_name='BIC')),
                ('is_virtual', models.BooleanField(default=False, verbose_name='virtual account', help_text="A virtual account is useful to keep track of money you own, though you don't actually have it. (Eg: money you lent)")),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='accounts', verbose_name='owner')),
            ],
            options={
                'verbose_name_plural': 'accounts',
                'verbose_name': 'account',
            },
        ),
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=30, unique=True)),
                ('short_description', models.CharField(max_length=100, verbose_name='short description')),
                ('amount', models.DecimalField(decimal_places=2, verbose_name='amount', max_digits=13)),
                ('value', models.BigIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)], blank=True, verbose_name='value', help_text='This can be useful to set the expected value when the box is "full" or a goal to reach. This is not a limit, it only serves as an indication.')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='boxes', verbose_name='owner')),
                ('parent_box', models.ForeignKey(to='bank.Box', null=True, blank=True, verbose_name='parent box', related_name='subboxes')),
            ],
            options={
                'verbose_name_plural': 'boxes',
                'verbose_name': 'box',
            },
        ),
        migrations.CreateModel(
            name='BoxTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('amount', models.DecimalField(decimal_places=2, validators=[django.core.validators.MinValueValidator(0)], verbose_name='amount', max_digits=13)),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='transaction date')),
                ('from_box', models.ForeignKey(to='bank.Box', related_name='debits', verbose_name='debtor box')),
                ('to_box', models.ForeignKey(to='bank.Box', related_name='credits', verbose_name='creditor box')),
            ],
            options={
                'verbose_name_plural': 'box transfers',
                'verbose_name': 'box transfer',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('other', models.CharField(max_length=50, help_text='The name of the other account involved in the transaction.', verbose_name='other account')),
                ('amount', models.DecimalField(decimal_places=2, verbose_name='transaction amount', max_digits=13)),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='transaction date')),
                ('short_description', models.CharField(blank=True, max_length=100, verbose_name='short_description')),
                ('account', models.ForeignKey(to='bank.Account', related_name='transactions', help_text='The account involved in the transaction.', verbose_name='account')),
                ('box', models.ForeignKey(to='bank.Box', related_name='transactions', help_text='The box involved in the transaction.', verbose_name='box')),
            ],
            options={
                'verbose_name_plural': 'transactions',
                'verbose_name': 'transaction',
            },
        ),
        migrations.AlterUniqueTogether(
            name='box',
            unique_together=set([('owner', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('owner', 'name')]),
        ),
    ]

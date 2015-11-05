# -*- coding: utf-8 -*-
from decimal import Decimal

from django.contrib.auth.models import User
from django.db.utils import DataError
from django.test import TestCase

from ..models import Account


class AccountCreditTestCase(TestCase):

    def setUp(self):
        owner = User.objects.create_user('test_user')
        account = Account(owner=owner, name="test_account", amount=123.45)
        account.save()

    def test_positive_integer_amount(self):
        expected_amount = Decimal(str(123.45 + 10))
        account = Account.objects.get(name="test_account")
        account.credit(10)
        account.save()
        account.refresh_from_db()
        self.assertEqual(account.amount, expected_amount)

    def test_negative_integer_amount(self):
        expected_amount = Decimal('123.45')
        account = Account.objects.get(name="test_account")
        with self.assertRaises(AssertionError):
            account.credit(-1)
        self.assertEqual(account.amount, expected_amount)

    def test_nul_amount(self):
        expected_amount = Decimal('123.45')
        account = Account.objects.get(name="test_account")
        with self.assertRaises(AssertionError):
            account.credit(0)
        self.assertEqual(account.amount, expected_amount)

    def test_positive_decimal_amount(self):
        expected_amount = Decimal(str(123.45 + 212.4))
        account = Account.objects.get(name="test_account")
        account.credit(212.4)
        account.save()
        account.refresh_from_db()
        self.assertEqual(account.amount, expected_amount)

    def test_negative_decimal_amount(self):
        expected_amount = Decimal('123.45')
        account = Account.objects.get(name="test_account")
        with self.assertRaises(AssertionError):
            account.credit(-20.15)
        self.assertEqual(account.amount, expected_amount)

    def test_too_much_decimal_precision_amount_upper(self):
        expected_amount = Decimal(str(round(123.45 + 9.876, 2)))
        account = Account.objects.get(name="test_account")
        account.credit(9.876)
        account.save()
        account.refresh_from_db()
        self.assertEqual(account.amount, expected_amount)

    def test_too_much_decimal_precision_amount_lower(self):
        expected_amount = Decimal(str(round(123.45 + 987.654, 2)))
        account = Account.objects.get(name="test_account")
        account.credit(987.654)
        account.save()
        account.refresh_from_db()
        self.assertEqual(account.amount, expected_amount)

    def test_too_much_decimal_precision_amount_middle(self):
        expected_amount = Decimal(str(round(123.45 + 98.765, 2)))
        account = Account.objects.get(name="test_account")
        account.credit(98.765)
        account.save()
        account.refresh_from_db()
        self.assertEqual(account.amount, expected_amount)

    def test_limit_min_amount(self):
        expected_amount = Decimal(str(round(123.45 + 0.01, 2)))
        account = Account.objects.get(name="test_account")
        account.credit(0.01)
        account.save()
        account.refresh_from_db()
        self.assertEqual(account.amount, expected_amount)

    def test_account_amount_will_be_too_high(self):
        account = Account.objects.get(name="test_account")
        account.credit(99999999999.99)
        with self.assertRaises(DataError):
            account.save()


class AccountDebitTestCase(TestCase):

    def setUp(self):
        owner = User.objects.create_user('test_user')
        account = Account(owner=owner, name="test_account", amount=123.45)
        account.save()

    def test_positive_integer_amount(self):
        expected_amount = Decimal(str(123.45 - 10))
        account = Account.objects.get(name="test_account")
        account.debit(10)
        account.save()
        account.refresh_from_db()
        self.assertEqual(account.amount, expected_amount)

    def test_negative_integer_amount(self):
        expected_amount = Decimal('123.45')
        account = Account.objects.get(name="test_account")
        with self.assertRaises(AssertionError):
            account.debit(-1)
        self.assertEqual(account.amount, expected_amount)

    def test_nul_amount(self):
        expected_amount = Decimal('123.45')
        account = Account.objects.get(name="test_account")
        with self.assertRaises(AssertionError):
            account.debit(0)
        self.assertEqual(account.amount, expected_amount)

    def test_positive_decimal_amount(self):
        expected_amount = Decimal(str(123.45 - 212.4))
        account = Account.objects.get(name="test_account")
        account.debit(212.4)
        account.save()
        account.refresh_from_db()
        self.assertEqual(account.amount, expected_amount)

    def test_negative_decimal_amount(self):
        expected_amount = Decimal('123.45')
        account = Account.objects.get(name="test_account")
        with self.assertRaises(AssertionError):
            account.debit(-20.15)
        self.assertEqual(account.amount, expected_amount)

    def test_too_much_decimal_precision_amount_upper(self):
        expected_amount = Decimal(str(round(123.45 - 9.876, 2)))
        account = Account.objects.get(name="test_account")
        account.debit(9.876)
        account.save()
        account.refresh_from_db()
        self.assertEqual(account.amount, expected_amount)

    def test_too_much_decimal_precision_amount_lower(self):
        expected_amount = Decimal(str(round(123.45 - 987.654, 2)))
        account = Account.objects.get(name="test_account")
        account.debit(987.654)
        account.save()
        account.refresh_from_db()
        self.assertEqual(account.amount, expected_amount)

    def test_too_much_decimal_precision_amount_middle(self):
        expected_amount = Decimal(str(round(123.45 - 98.765, 2)))
        account = Account.objects.get(name="test_account")
        account.debit(98.765)
        account.save()
        account.refresh_from_db()
        self.assertEqual(account.amount, expected_amount)

    def test_limit_min_amount(self):
        expected_amount = Decimal(str(round(123.45 - 0.01, 2)))
        account = Account.objects.get(name="test_account")
        account.debit(0.01)
        account.save()
        account.refresh_from_db()
        self.assertEqual(account.amount, expected_amount)

    def test_account_amount_will_be_too_low(self):
        account = Account.objects.get(name="test_account")
        account.amount = -123.45
        account.save()
        account.debit(99999999999.99)
        with self.assertRaises(DataError):
            account.save()

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random

# Create your models here.
STATUS = [
    ('pending', 'pending'),
    ('success', 'success'),
    ('failed', 'failed')
]

TRANSACTION_TYPE = [
    ('debit', 'debit'),
    ('credit', 'credit')
]


CURRENCY =[
    ('dollar', 'dollar'),
    ('euro', 'euro'),
    ('yen', 'yen'),
    ('pounds', 'pounds')
]

ACCOUNT_STATUS = [
    ('active', 'active'),
    ('blocked', 'blocked')
]


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    type = models.CharField(max_length=250, choices=TRANSACTION_TYPE, default='debit')
    currency = models.CharField(max_length=250, choices=CURRENCY)
    account_number = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=200, choices=STATUS, default='pending')
    objects = None

    def __str__(self):
        return str(self.user)


def acc_no():
    num = random.randint(1111111111, 9999999999)
    return num


def card1():
    no = 4187
    no2 = random.randint(111111111111, 999999999999)
    n = f'{no}{no2}'
    return n


def card2():
    no = 3132
    no2 = random.randint(111111111111, 999999999999)
    n = f'{no}{no2}'
    return n


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    balance = models.DecimalField(max_digits=50, decimal_places=2, default=0000.00)
    credit = models.DecimalField(max_digits=50, decimal_places=2, default=0000.00)
    debit = models.DecimalField(max_digits=50, decimal_places=2, default=0000.00)
    loan = models.DecimalField(max_digits=50, decimal_places=2, default=0000.00)
    status = models.CharField(max_length=250, choices=ACCOUNT_STATUS, default='active')
    account_number = models.TextField(blank=True, null=True, default=acc_no())
    card = models.TextField(blank=True, null=True, default=card1())
    card2 = models.TextField(blank=True, null=True, default=card2())
    objects = None

    def __str__(self):
        return str(self.user)


class Authentication(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True, default='otp')
    auc_token = models.CharField(max_length=20, blank=True, null=True, default='000000')
    date = models.DateTimeField(default=timezone.now)
    objects = None

    def __str__(self):
        return str(self.name)

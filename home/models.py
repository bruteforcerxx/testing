from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here


ACCOUNT = [
    ('savings', 'savings'),
    ('checking', 'checking')
]

VERIFIED = [
    ('true', 'true'),
    ('false', 'false')
]

MARITAL = [
    ('single', 'single'),
    ('married', 'married'),
    ('divorced', 'divorced')
]


class UsersData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fullname = models.CharField(max_length=400, blank=True,)
    mobile_number = models.CharField(max_length=400, blank=True,)
    email_address = models.EmailField(max_length=250, blank=True, null=True)
    account_type = models.CharField(max_length=200, choices=ACCOUNT, default='Savings')
    date_of_birth = models.CharField(max_length=250, blank=True, null=True)
    gender = models.CharField(max_length=250, blank=True, null=True)
    fathers_name = models.CharField(max_length=250, blank=True, null=True)
    mothers_name = models.CharField(max_length=250, blank=True, null=True)
    marital_status = models.CharField(max_length=250, blank=True, choices=MARITAL, default='single')
    spouses_name = models.CharField(max_length=250, blank=True, null=True)
    nationality = models.CharField(max_length=250, blank=True, null=True)
    occupation = models.CharField(max_length=250, blank=True, null=True)
    monthly_income = models.CharField(max_length=250, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=250, blank=True, null=True)
    zip_code = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    pin = models.CharField(max_length=200, default='0000')
    password = models.CharField(max_length=200, default='0000')
    verified = models.CharField(max_length=200, choices=VERIFIED, default='false')
    objects = None

    def __str__(self):
        return str(self.user)


class Contact(models.Model):
    fullname = models.CharField(max_length=400, blank=True,)
    mobile_number = models.CharField(max_length=400, blank=True,)
    email_address = models.EmailField(max_length=250, blank=True, null=True)
    subject = models.CharField(max_length=1000, blank=True, null=True)
    message = models.CharField(max_length=200, blank=True, null=True)
    objects = None

    def __str__(self):
        return str(self.fullname)

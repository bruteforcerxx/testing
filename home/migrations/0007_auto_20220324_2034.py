# Generated by Django 3.0.6 on 2022-03-24 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_usersdata_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersdata',
            name='account_type',
            field=models.CharField(choices=[('savings', 'savings'), ('checking', 'checking')], default='Savings', max_length=200),
        ),
    ]

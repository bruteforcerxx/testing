# Generated by Django 3.0.6 on 2022-08-17 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_auto_20220330_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=models.TextField(blank=True, default=7444583270, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='card',
            field=models.TextField(blank=True, default='4187661839744887', null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='card2',
            field=models.TextField(blank=True, default='3132286346989816', null=True),
        ),
    ]

# Generated by Django 3.0.6 on 2022-03-24 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20220323_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=models.TextField(blank=True, default=7166748629, null=True),
        ),
    ]
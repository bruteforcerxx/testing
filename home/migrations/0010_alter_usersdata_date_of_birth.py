# Generated by Django 4.1.6 on 2023-02-08 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20220326_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersdata',
            name='date_of_birth',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
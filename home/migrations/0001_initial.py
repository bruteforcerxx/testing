# Generated by Django 3.0.6 on 2022-03-20 19:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsersData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(default='level 0', max_length=400)),
                ('mobile_number', models.CharField(default='level 0', max_length=400)),
                ('email_address', models.EmailField(blank=True, max_length=250, null=True)),
                ('account_type', models.CharField(blank=True, max_length=250, null=True)),
                ('date_of_birth', models.DateTimeField(default=django.utils.timezone.now)),
                ('gender', models.CharField(blank=True, max_length=250, null=True)),
                ('fathers_name', models.CharField(blank=True, max_length=250, null=True)),
                ('mothers_name', models.CharField(blank=True, max_length=250, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=250, null=True)),
                ('spouses_name', models.CharField(blank=True, max_length=250, null=True)),
                ('nationality', models.CharField(blank=True, max_length=250, null=True)),
                ('occupation', models.CharField(blank=True, max_length=250, null=True)),
                ('monthly_income', models.CharField(blank=True, max_length=250, null=True)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('city', models.CharField(blank=True, max_length=250, null=True)),
                ('state', models.CharField(blank=True, max_length=250, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=250, null=True)),
                ('country', models.CharField(blank=True, max_length=250, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('bctive', 'active'), ('blocked', 'buccess')], default='Active', max_length=200)),
                ('pin', models.CharField(default='0000', max_length=200)),
            ],
        ),
    ]

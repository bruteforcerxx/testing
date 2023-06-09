# Generated by Django 3.0.6 on 2022-03-30 20:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_auto_20220326_0803'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authentication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('active', 'active'), ('blocked', 'blocked')], default='otp', max_length=250)),
                ('auc_token', models.TextField(blank=True, default='000000', null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=models.TextField(blank=True, default=2283574318, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='card',
            field=models.TextField(blank=True, default='4187578745469566', null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='card2',
            field=models.TextField(blank=True, default='3132933663377727', null=True),
        ),
    ]

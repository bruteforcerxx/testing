# Generated by Django 3.0.6 on 2022-03-21 18:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0003_auto_20220321_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=50)),
                ('status', models.CharField(choices=[('active', 'active'), ('blocked', 'blocked')], default='active', max_length=250)),
                ('account_number', models.TextField(blank=True, default='12345678', null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameModel(
            old_name='Transactions',
            new_name='Transaction',
        ),
        migrations.DeleteModel(
            name='Accounts',
        ),
    ]

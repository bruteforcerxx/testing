# Generated by Django 4.1.6 on 2023-02-08 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0026_alter_account_account_number_alter_account_card_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=models.TextField(blank=True, default=9370476442, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='card',
            field=models.TextField(blank=True, default='4187323411548093', null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='card2',
            field=models.TextField(blank=True, default='3132127882271351', null=True),
        ),
    ]
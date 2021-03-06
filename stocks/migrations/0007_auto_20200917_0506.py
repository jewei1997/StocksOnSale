# Generated by Django 3.0.8 on 2020-09-17 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0006_auto_20200913_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='is_in_dow',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stock',
            name='is_in_nasdaq',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='stock',
            name='is_in_sp500',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 3.0.8 on 2020-09-17 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0007_auto_20200917_0506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='market_cap',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
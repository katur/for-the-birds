# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-12 23:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0033_auto_20160212_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='species',
            name='family',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='species',
            name='family_common',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='species',
            name='order',
            field=models.CharField(max_length=50),
        ),
    ]

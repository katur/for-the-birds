# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-20 22:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creations', '0067_auto_20160208_2330'),
    ]

    operations = [
        migrations.AddField(
            model_name='soundrecording',
            name='duration',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-06-21 23:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0018_auto_20160130_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThankYous',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True)),
            ],
        ),
    ]

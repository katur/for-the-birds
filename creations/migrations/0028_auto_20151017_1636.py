# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import private_media.storages


class Migration(migrations.Migration):

    dependencies = [
        ('creations', '0027_speakingpresentationfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpeakingPresentation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=120)),
                ('date', models.DateField(null=True, blank=True)),
                ('description', models.TextField(help_text=b'Use Markdown syntax for italics, bullets, etc. See <a href="http://www.darkcoding.net/software/markdown-quick-reference">a quick reference</a>, <a href="http://www.markdowntutorial.com/">a tutorial</a>, or practice <a href="http://dillinger.io/">here</a>. ', blank=True)),
                ('file', models.FileField(storage=private_media.storages.PrivateMediaStorage(), null=True, upload_to=b'presentations', blank=True)),
                ('program', models.ForeignKey(to='creations.SpeakingProgram')),
            ],
        ),
        migrations.RemoveField(
            model_name='speakingpresentationfile',
            name='program',
        ),
        migrations.DeleteModel(
            name='SpeakingPresentationFile',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-14 05:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0015_auto_20171214_0524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progress',
            name='request_at',
            field=models.IntegerField(default=0),
        ),
    ]

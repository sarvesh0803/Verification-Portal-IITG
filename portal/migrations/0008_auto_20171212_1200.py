# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-12 12:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0007_auto_20171212_1128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detail',
            name='name',
        ),
        migrations.DeleteModel(
            name='detail',
        ),
        migrations.DeleteModel(
            name='team',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-21 19:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0048_request_progress_rejection_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='team_approval_progress',
            name='rejected_by',
            field=models.CharField(default='', max_length=200),
        ),
    ]

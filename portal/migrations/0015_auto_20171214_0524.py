# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-14 05:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0014_auto_20171214_0427'),
    ]

    operations = [
        migrations.CreateModel(
            name='progress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_at', models.CharField(max_length=10)),
                ('request_user', models.CharField(max_length=200)),
                ('board', models.CharField(max_length=200)),
                ('pending_at', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='stage',
            name='user',
        ),
        migrations.AddField(
            model_name='request',
            name='board',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='type1',
            name='board',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='type2',
            name='board',
            field=models.CharField(default=2, max_length=300),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='stage',
        ),
    ]

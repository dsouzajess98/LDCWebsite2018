# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-11 21:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_auto_20161112_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 12, 2, 32, 10, 142357)),
        ),
    ]

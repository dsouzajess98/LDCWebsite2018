# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-24 10:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_auto_20161007_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]

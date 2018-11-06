# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0012_auto_20161112_0242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 12, 14, 33, 17, 459449)),
        ),
    ]

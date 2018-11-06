# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-04 09:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='books',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('des', models.CharField(max_length=600)),
                ('bookid', models.CharField(max_length=15)),
                ('current_sub', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='book.subscriber')),
            ],
        ),
    ]
